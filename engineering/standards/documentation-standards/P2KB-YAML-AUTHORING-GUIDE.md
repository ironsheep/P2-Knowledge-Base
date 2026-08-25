# P2KB YAML Authoring Guide

**Surface:** the shipped knowledge base, `deliverables/ai/P2/**.yaml`.
**Audience:** `agent-consumer` — a remote agent generating P2 code from these files.
**Added:** 2026-08-24.

---

## Why this guide exists

Every other surface in this project had a conformance guide. The one that did
not was the KB — the most-consumed deliverable we ship, and the only one whose
reader cannot push back.

That asymmetry was invisible until an agent could not work out how to use
pull-ups from the published KB, and the investigation found seven defects
(F-321…F-327) that had passed every release. None of them were caught by a
reader, a review, or a validator, because nothing in the release path was
looking at whether the KB says true things — only whether it parses and its
keys resolve.

**Every rule below is the general form of a specific defect that shipped.** None
is a preference. Where a rule cites a finding, that finding is the evidence, and
the register carries the detail.

## The bar this surface is held to

`{{DELIVERABLE_AUDIENCE}}` marks this surface **agent-consumer**, which sets a
stricter bar than the manuals get: **cite the authority or omit the entry.**

A human reading a manual can weigh a hedge. An agent cannot. It has no way to
discount "approximately", "typically", or "should be" — it reads a claim, emits
code, and the wrong fact becomes silently authoritative in someone's project. So
an entry shipped marked-unverified is not a cautious entry; it is a defect
wearing a caveat.

---

## R1 — Match the source's wording. Do not translate it into what a reader expects.

The source says what a thing **does**. Rewriting that into the nearest familiar
concept is not clarification — it changes the claim.

> **F-321.** `P_HIGH_15K` is *"Drive high 15kΩ"* — a drive-strength selector,
> active only while the pin drives. Sixteen constants were documented as
> *"15kΩ pull-up"*, a bias resistor that is always active. The P2 has no pull-up
> resistors. The rename read as a simplification and was an inversion, and every
> example built on top of it was wrong.

When a reader's *intent* maps to something the chip does differently, document
the **idiom** — the real composition that achieves it — never a component the
chip does not have.

## R2 — Every quantitative claim carries its source. No exceptions for round numbers.

A number without a citation cannot be distinguished from a number someone
inferred, and inference is how fabrication enters.

> **F-327.** `io_pin_timing.yaml` stated a six-step drive ladder, an impedance
> table, a bit layout, and a whole programmable slew-rate feature. None of it
> exists in any source; "slew" appears zero times across the Silicon Doc, the
> Spin2 sources, and the smart-pins catalog. The same file cites the Parallax
> Datasheet and Silicon Doc v35 in neighbouring sections — it knew how to cite,
> and these blocks carried no `source:` field at all.

**An uncited quantitative block in a file that cites elsewhere is the tell.** It
is mechanically detectable and it is gated.

### R2a — A citation is not a token. It names the document that states THIS claim.

The instrument matches on the **presence of a token** — the bare word *datasheet*
anywhere in the block — never on whether the sentence attributes the block to a
document. Four different things have scored as citations: a board revision
(`Rev C`), a power supply `source:`, a filename slug, and a **deferral**.

> **F-348.** `max_current_total: "Check datasheet for package limits"` scored the
> whole block as cited. So the block sailed through two separate purges while
> asserting `max_current_per_pin: "150mA"` against the datasheet's stated
> *"Max. allowable current per I/O pin ±30 mA"* — **five times the absolute
> maximum, in the exact number a reader uses to size an LED series resistor.**

*"Check the datasheet for…"*, *"see the datasheet"*, *"per the manual"* are
pointers **away** from the block. A citation points **at** a source **for the
claim being made**, and locates it — document, edition, and `file:line` or page.
**A pointer away from the block is not a citation, and a green gate does not make
it one.**

## R3 — An unsourced claim is deleted, not rewritten.

There is a strong pull toward "fixing" a wrong block by improving its wording.
If no source states the thing, there is nothing to align it toward, and a
rewritten fabrication is still a fabrication with better prose.

Correcting applies where a real mechanism was described wrongly (R1). Deleting
applies where the mechanism does not exist (R2). Decide which before editing.

### R3a — Repair source-first, never claim-first.

Opening the block and then hunting for something that supports it is how a
loosely-related citation gets stapled to a wrong claim: the search is steered by
the answer already on the page, and the nearest plausible document wins.

Read the **source** first and write down what it states. *Then* look at the block.
The order matters because it changes what you are able to notice — claim-first
asks *"can I justify this?"*, and there is almost always something that says
nearly this, in some edition, about some neighbouring thing.

## R4 — One fact lives in one file. Everything else points at it.

> **F-323.** The two `basic-io.yaml` files gave contradictory mechanisms for the
> same feature — one said `PINSTART()`, the other said `WRPIN`. Both were wrong,
> in different directions. **F-321** shipped the same mislabel in six files.

Correcting duplicated text in every copy preserves the arrangement that drifted.
Remove the duplicate, keep one home, and point. **Deletion is the correction.**

**Pointing has a shape constraint, and it is not obvious.** `audit-constant-fidelity.py`
reads any `NAME: description` line as a **definition**. So a second file that
lists constants the natural way becomes a second definition *home* even when its
author intended a pointer — which re-manufactures this very defect inside the
work chartered to end it. When a new file must describe constants it does not
own, state the material **by encoding** — bit ranges, values, field structure —
and let the one definition home carry the `NAME: description` lines. Verify it
mechanically: the tool must attribute **zero** definitions to the new file.

Cross-references use **full repo-absolute paths**. A bare relative path such as
`concepts/basic-io.yaml` matched two different files in this set, and a `content_base:`
declared at the top of a file is not a resolution rule — neighbouring entries in
the same block pointed outside it.

## R5 — Define what you use.

A constant referenced by the KB and defined nowhere in it leaves the reader with
a token and no meaning.

> **F-325.** 41 constants were referenced across the shipped set and defined in
> none of it — `P_ADC_1X` in seven files, `P_ADC_GIO` and `P_ADC_VIO` in seven
> each. The full definition tables existed in the ingestion tree the whole time
> and had never been promoted.

### R5a — Findability is part of correctness. A fact nobody can reach is not shipped.

`generate-p2kb-index.py` harvests **top-level `aliases:` only**. Every `P_*`
constant this set defines lived in a file that had no `aliases:` block, so not
one of them was reachable by name through the published index — defined,
correct, cited, and invisible to the consumer who needed it.

**Defining a fact satisfies the instrument; being reachable is what serves the
reader.** When you add definitions to a file, add or extend its top-level
`aliases:` in the same edit, and confirm the name resolves through the index
afterwards — the index is regenerated, so a definition added without it is
findable to you and to nobody else.

## R6 — A deferral in a source is a work item, not an answer.

> **F-326.** `wrpin.yaml` expands three of its six D-operand fields in full and
> stubs the one carrying the pin configuration: *"13-bit low-level pin control"*.
> The Silicon Doc defers at exactly that field — *"In the Spin2 documentation,
> there are many predefined labels documented"* — and the ingestion followed the
> source faithfully to the pointer and then stopped, even though the target was
> itself already ingested.

Follow the pointer, or record a gap. Never inherit the deferral silently: the
reader lands on the stub with no way to know an answer exists elsewhere.

## R7 — State bit positions. A field name is not a field.

> **F-324.** `bits_M_6_0: "Control drive strength"` was wrong at both ends —
> drive-high is `M[5:3]`, drive-low is `M[2:0]`, and `M[6]` is output polarity.
> Two sources independently confirm the real split; the KB's range annexed the
> polarity bit and erased the high/low structure that makes the field usable.

Where a field has sub-fields, give each its range. An agent composing a mode
word needs positions, not a label.

## R8 — Every code example must work exactly as written.

An example is executable specification. A reader pastes it.

> **F-322.** Eight worked examples configured a drive strength and then floated
> the pin on the next line. `DIR=0` disables the output, so the setting they had
> just made was inactive — every one of them shipped a non-functional pattern
> under a comment claiming it worked.

Compile every example with `pnut-ts` (add `-d` where it carries `debug()`), and
**check the semantics separately**: a clean compile proves legality, never that
the code does what its comment says.

## R9 — No inference, no derivation.

Aligning an entry to an authority it contradicts is correct. Inventing a value
or a claim that no source states — by computation, reasoning, or *"it must
logically be"* — is not. If a change can only be justified by inference, it is a
gap to source, not content to ship.

This is the register's own standing rule, restated here because this is the
surface where breaking it does the most damage.

## R10 — A verify criterion can rot into a trap. Check what a hit ASSERTS, never that a phrase is absent.

The criterion that proves a purge worked is almost always phrase-absence, and it
is correct **exactly once** — at the moment the fabrication is removed and before
the correction is written.

Then the correction gets written, and a good correction **states the denial**.
*"The P2 has no internal pull-up/pull-down resistor network"* contains the phrase
the criterion forbids. Re-run the original check and it now fails; act on that
failure and you delete the denial and restore the silence the fabrication lived
in to begin with.

> Both `basic-io.yaml` files return **5** hits for pull-up/pull-down, and all five
> are correct: the denial, the two corrected substitute idioms, and a note
> recording what the pre-purge form said and why it was wrong. **F-333** is the
> same inversion — `io_pin_timing.yaml` was recorded as returning **0** hits for
> *slew* when the fabrication was cut, and now returns two, both denials.

**Write the criterion as "no hit asserts X", never "X does not appear."** A
purge-era criterion carried forward unchanged is how the original fabrication
survived two purges: the check that proved the removal is the check that erases
the correction.

---

## The gate

| Instrument | What it enforces |
|---|---|
| `audit-constant-fidelity.py` | R1, R4, R5 — named-constant descriptions against the source, and the KB against itself |
| `audit-yaml-claim-sourcing.py` | R2, R3 — quantitative claims carrying a `source:` |
| `pnut-ts` (`-d` for `debug()`) | R8, legality half only |
| `verify-yaml-format.py` · `validate-crossref-keys.py` | parse and cross-reference integrity |

**What a green gate does NOT certify.** These instruments check *named* constants
and *quantitative* claims. Prose that describes a behaviour without naming a
constant or stating a number passes untouched — which is exactly how F-327 sat in
a released file. **R3a, R5a, R6, R7, R9 and R10 have no instrument** and are held
by review.

Two coverage holes are known and specific, and both have already shipped a defect:

- **The citation side matches a token, not an attribution** (R2a). A block scores
  as cited when the word *datasheet* appears in it — including in a deferral that
  points the reader away. Until that is repaired, a green claim-sourcing run says
  a citation-shaped string is present, never that the claim is attributed.
- **`validate-crossref-keys.py` scans a fixed list of TOP-LEVEL fields only.** A
  citation nested inside another mapping — `knowledge_progression:`,
  `next_steps:`, a `content:` entry — is never examined, so it cannot be reported
  unresolved no matter what it points at. Both getting-started guides routed every
  new agent through such a citation, and the validator was green throughout.

**Name coverage is not semantic coverage, and neither is description coverage.**
A clean run means "not caught by these checks", never "correct" — and for a field
an instrument never reads, it does not even mean that.
