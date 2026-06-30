# IOSP Release Campaign Plan

> **Status:** active (set 2026-06-30). Drives `active_element =
> manual:p2-io-and-smart-pins-user-guide`. Supersedes the `plan_iosp_release_sequence`
> context note (which this doc now records durably).

## Goal

Release the **P2 I/O & Smart Pins User Guide (IOSP)** — but **last**, after folding in
three document-informing inputs, so IOSP ships **once, fully informed**. Two of those
inputs are *new app notes* taken all the way to PDF; the third is a focused USB study.

**Current IOSP state:** toward-first-release overhaul done (cross-ref filter +
circuitikz diagrams + ~33 edits, 387→382pp, daemon-verified; prepare-manual staged;
**committed, NOT released**). See memory `project_iosp_user_guide_state`.

## Order rationale (Stephen)

Gather **all** document-informing studies *before* closing the release. Each input has
a **boundary-determination** step that decides what is foundational (→ enriches IOSP)
vs. advanced technique (→ becomes an app note). IOSP releases only after every
foundational fork has been folded in.

## The three inputs (each a release-blocking IOSP input)

### Input 1 — USB study → IOSP augmentation
- **Study** the OBEX USB code (e.g. **USBnew**, **USB HID Driver**) plus the P2 USB
  smart-pin mode (`%11011`, host/device).
- **Delineate** foundational USB smart-pin mechanics (→ IOSP) from the hard
  *composition* of a working device/host (→ a future standalone USB app note — the
  roster's Standalone item; **not** authored in this campaign, only its IOSP-relevant
  findings).
- **Augment IOSP** with the USB smart-pin content the study surfaces.
- *(This is the example-mining front-end for the roster's Standalone USB note; the
  note itself stays a candidate.)*

### Input 2 — P2AN003: DAC & Analog Signal Generation (Family A1)
- Working doc: `engineering/document-production/app-notes/P2AN003/P2AN003-NOTES.md`.
- Run the §2 boundary playbook: mine DAC/sound examples → **decide the IOSP-vs-note
  split** → **augment IOSP** with foundational DAC additions → author the
  advanced-technique note (+ YAML companion) → **take to PDF**.

### Input 3 — P2AN004: Frequency / Period / Pulse Measurement (Family A2)
- Working doc: `engineering/document-production/app-notes/P2AN004/P2AN004-NOTES.md`.
- Same playbook: mine measurement examples → **decide the split** → **augment IOSP**
  with foundational measurement additions → author the note (+ YAML companion) →
  **take to PDF**.

> **Resolved open question:** the "two IOSP-related app notes" are these two **new**
> Family-A notes (P2AN003 DAC, P2AN004 Freq/Period/Pulse) — **not** the parked
> P2AN001 (ADC, which already enriched IOSP Ch.16) or P2AN002 (CORDIC, Math-family,
> separate track #140).

## Sequence

1. **USB study** (Input 1) → fold USB findings into IOSP.
2. **P2AN003 DAC** (Input 2) → boundary split → IOSP DAC enrichment → author → PDF.
3. **P2AN004 Freq/Period/Pulse** (Input 3) → boundary split → IOSP measurement
   enrichment → author → PDF.
4. **Augment IOSP** = the union of the three foundational forks (USB + DAC + measurement).
5. **Release IOSP last** via `release-manual`: verify the PDF (page count, outline,
   key sections, compile log), promote CHANGELOG, update the deliverables README +
   roster, record the Platform Freshness Ledger PUBLISH line, commit/tag.

Each app note also ships its own PDF (Inputs 2 & 3 deliverables) and example-library
ZIP, and is registered in the dashboards (see below). The two new notes follow the
P2AN001/P2AN002 doc-class shape + YAML-companion schema.

## What "augment IOSP" means (Stephen, 2026-06-30)

For **both** app notes: once the IOSP-vs-note split is decided, **augment IOSP content
with any desired foundational additions** surfaced by that note's example-mining. The
note keeps the advanced technique; IOSP keeps the foundation. The boundary is made
objective by the examples, not guessed.

## Tracking-dashboard updates (done at stand-up 2026-06-30)

- **Planned / in-production:** P2AN003 + P2AN004 added to
  `engineering/document-production/PUBLICATION-ROSTER.md` (Application Notes section),
  its README mirror, `app-notes/README.md` (The series), and
  `engineering/analysis/p2-app-note-roster.md` (A1/A2 → numbered + in-campaign).
- **About to release:** IOSP carried as the campaign's terminal release; the two notes
  move to "about to release" as each reaches a verified PDF.

## Dependencies / notes

- P2AN002 (CORDIC) authoring (#140) is a **separate Math-family track**; it does not
  gate this campaign (CORDIC doesn't touch IOSP).
- The shared **example-mining front-end** (processing community code to find doc
  boundaries) is the roster's two-pipeline model (§6) — a candidate standing activity.
