# IOSP Release Campaign — Sprint Plan

> **Status:** ready for `sprint-start` (planned 2026-06-30). Drives
> `active_element = manual:p2-io-and-smart-pins-user-guide`. Supersedes the interim
> `IOSP-RELEASE-CAMPAIGN-PLAN.md` (renamed to this canonical sprint-plan).
> **Type:** plan (ship commitment), not a study.

## Goal

Release the **P2 I/O & Smart Pins User Guide (IOSP)** — but **last**, after three
boundary-determination passes fold their *foundational* findings into the guide. Two
of those passes also emit app notes (P2AN003, P2AN004) taken to verified PDF; the
third (USB) is IOSP-augmentation only. IOSP ships **once, fully informed**.

**Current IOSP state:** toward-first-release overhaul done (cross-ref filter +
circuitikz diagrams + ~33 edits, 387→382pp, daemon-verified; prepare-manual staged;
**committed, NOT released**). See memory `project_iosp_user_guide_state`.

## Resolved scope decisions (Stephen, 2026-06-30)

- **App-note release coupling (Q1):** P2AN003/P2AN004 reach **verified PDF** in this
  campaign (strengthening their IOSP contribution) but their **public release is NOT
  scheduled** — IOSP releases first; the notes release later.
- **USB depth (Q2):** **IOSP augmentation only.** Study *both* OBEX USB objects in
  detail to learn how much belongs in IOSP — that is the fundamental goal. No
  standalone USB app note; any future USB product (working drivers — possibly what the
  OBEX objects already are, untested) is a **later** decision, out of scope now.
- **Versions (Q3):** everything **v0.1.0**; IOSP first release **v1.0.0** is grabbed by
  `release-manual` at release time, not set here.
- **Fan-out architecture (Stephen, 2026-06-30):** the three boundary passes **fan out
  in parallel**, reduce through a **single-writer merge** (the Conductor's merge
  pattern), then **document generation is a two-task tail** after the merge. The
  linchpin is a **standard mergeable output contract** from `mine-and-delineate` so
  the three results reduce uniformly. The skill is **in-repo**, not an augmentation of
  the central `ingest-conductor`.

---

## §0. Author the `mine-and-delineate` in-repo skill

**Why.** The "process community examples → delineate foundational (→owning manual) vs
advanced (→app note)" front-end has run twice already (P2AN001 ADC, P2AN002 CORDIC)
and runs **three more times** this campaign. That is the extraction window: enough
proven practice to capture the real shape, plus immediate live validation. It is a
*distinct activity from KB-fact ingestion* (the roster, §6, names it a candidate
standing activity), so it gets its **own in-repo skill** — not an overload of
`ingest-source`/`ingest-conductor`.

**Starting point.** The §2 playbook in `engineering/analysis/p2-app-note-roster.md`
(locate+download → study → delineate → fork). The two proven NOTES are the ground
truth to extract from: `app-notes/P2AN001/P2AN001-NOTES.md`,
`app-notes/P2AN002/P2AN002-NOTES.md` (esp. their "Boundary delineation" + "Sources to
mine" + "Source traceability" sections). Skill layout convention:
`.claude/skills/<name>/SKILL.md` (+ `project-overlay.md`).

**Target.** `.claude/skills/mine-and-delineate/SKILL.md` covering:
1. **Single-source mode** — one region: locate+download examples (OBEX #/QB/external)
   → study → delineate → emit the standard artifact.
2. **The mergeable output contract** *(the linchpin)* — a uniform
   **boundary-determination artifact** each run emits, structured so the merge reduces
   them identically: `{region, sources[], foundational-additions→owning-manual,
   advanced-recipes→app-note (may be empty), verification, open-questions}`.
3. **Fan-out / coordinator mode** — run N regions in parallel, then **reduce** the N
   artifacts into the owning manual via a single-writer merge, modeled on the proven
   `ingest-conductor` + `ingest-wrap-reduce` pattern (manifest + reduce). Document
   generation is explicitly **downstream of the merge**, not part of the fan-out.

**Integration points.** Feeds two pipelines (roster §6): the **manual-enrichment**
fork (prepare/finalize/release skills) and the **app-note** fork (authoring +
four-artifact YAML companion). Reads `deliverables/ai/P2/` + OBEX via `p2kb-obex-*`.

**Verification (normal / edge / error).**
- *Normal:* dry-run the skill's procedure against P2AN001 + P2AN002 — does it reproduce
  the boundary split we actually made? If not, the procedure is wrong.
- *Edge:* a region with **no app-note fork** (USB) — the artifact's advanced-recipes
  section is empty and no doc-gen task is appended; the skill must handle this.
- *Error:* two regions propose **overlapping** IOSP additions (USB + DAC both touching
  analog-pin config) — the merge step must detect and reconcile, not double-write.
- *Skill-evolution:* once the fan-out runs cleanly here, log "extract a
  boundary-conductor (central-promotion candidate), modeled on ingest-conductor" to
  `feedback_skill_evolution_candidates.md`.

---

## §1. Fan-out — boundary determination ×3 (USB, DAC, Freq)

Run `mine-and-delineate` in **fan-out mode** across the three regions in parallel.
Each emits the standard mergeable artifact.

### §1a. USB → IOSP USB augmentation (no app-note fork)
- **Why / goal.** Study both OBEX USB objects in detail to decide how much USB
  smart-pin content belongs in IOSP.
- **Sources to mine.** OBEX **USBnew**, **USB HID Driver** (cite by OBEX #; locate via
  `p2kb-obex-find`); P2 USB smart-pin mode `%11011` (host/device).
- **Starting point.** IOSP opus-master smart-pin chapter(s); `deliverables/ai/P2/`
  smart-pin mode YAMLs.
- **Output.** Artifact with **foundational USB additions → IOSP**, advanced-recipes
  **empty**, sources + open-questions. *(Untested OBEX driver maturity is an
  open-question, not a claim.)*
- **Verify.** Every USB claim sourced (no inference); any code `pnut_ts`-clean.

### §1b. P2AN003 — DAC & Analog Signal Generation (Family A1)
- **Working doc.** `app-notes/P2AN003/P2AN003-NOTES.md`.
- **Sources to mine.** QB "ADC→DAC" + "Analog Frequency to DAC"; sound-engine OBEX.
- **Output.** Artifact: foundational DAC → IOSP; advanced (dithering, streaming/DDS,
  synthesis) → P2AN003 recipes; sources + verification model.

### §1c. P2AN004 — Frequency / Period / Pulse Measurement (Family A2)
- **Working doc.** `app-notes/P2AN004/P2AN004-NOTES.md`.
- **Sources to mine.** QB TSL235R (freq); OBEX P2_rctime (pulse); quadrature.
- **Output.** Artifact: foundational measurement modes → IOSP; advanced worked
  instruments (tachometer, freq counter, ToF) → P2AN004 recipes; sources + verification.

**Verification (the fan-out as a whole).**
- *Normal:* three artifacts emitted in the common schema.
- *Edge:* USB artifact has an empty advanced section (handled, not an error).
- *Error:* no region silently drops a source it located (each artifact lists what it
  mined; a located-but-unstudied source is a finding, not an omission).

---

## §2. Merge / reduce → IOSP enrichment + re-audit

**Why.** All three foundational forks target the **same** IOSP opus-master — a
single-writer reduce prevents conflict and silent overlap.

- **Starting point.** The three §1 artifacts + IOSP opus-master
  (`manuals/p2-io-and-smart-pins-user-guide/opus-master/`, multi-part).
- **Target.** Integrate the union of foundational additions (USB + DAC + measurement)
  into IOSP opus-master, reconciling overlaps (e.g. shared analog-pin config). Edit the
  **opus-master**, never the workspace render (memory
  `feedback_edit_opus_master_not_workspace_render`).
- **Re-audit.** `document-audit` at **release depth** on IOSP against the current
  YAML/KB HEAD (drain gate) + itself; resolve findings via `document-finalize`.
- **Design-decisions to flag (overlay rule — wait for Stephen before editing):**
  app-note **YAML companions** are *new files* (P2AN003/P2AN004) — flag the companion
  schema (piloted on P2AN001/002 per `APP-NOTE-DESIGN-DECISIONS.md`) before authoring.
- **Verify.** *Normal:* IOSP reads coherently with the additions. *Edge:* overlapping
  USB/DAC additions reconciled to one section, no duplication. *Error:* audit drain
  gate GREEN (no actionable YAML corrections pending) before release is allowed.

---

## §3. Document-generation tail — P2AN003 + P2AN004 to verified PDF

Two tasks appended after the merge (independent files; parallel-capable, but PDF
generation is Forge handback so Stephen-paced).

- **For each note:** author `opus-master/<P2ANxxx>.md` + `front-matter.md` from its
  delineated advanced fork, per `APP-NOTE-CREATION-GUIDE.md` (techniques-catalog
  archetype likely; K=76; no ToC; examples-library ZIP; OBEX cites by #). Every
  example `pnut_ts`-clean (`-d` if `debug()`).
- **Produce PDF** via `prepare-manual` → PDF Forge; **verify the render** yourself
  (page count, outline, key sections, compile log — guard against silent content-drop).
- **Verify.** *Normal:* clean compile, 0 missing glyphs, outline complete. *Edge:*
  marker emoji + inline-ASCII gates pass. *Error:* any over-K line or non-ASCII inline
  span is an authorship defect fixed in source, not worked around.
- **Outcome:** both notes at **verified-PDF, v0.1.0** — release NOT scheduled (Q1).

---

## §4. IOSP release (terminal)

- **Why.** IOSP is now fully informed by all three forks.
- **Target.** `release-manual`: verify the IOSP PDF (page count, outline, sections,
  compile log), promote CHANGELOG, update deliverables README + `PUBLICATION-ROSTER`
  (move IOSP to Released), record the Platform Freshness Ledger PUBLISH line + roster
  status, surface commit/tag. **Version v1.0.0** grabbed here.
- **Adopt the cross-ref filter** + visual-audit (IOSP is the pilot; tracker
  `CROSSREF-FILTER-ADOPTION.md`).
- **Verify.** *Normal:* PDF complete + outline verified. *Edge:* shared-platform
  freshness — IOSP built on the current platform (it was behind `figures.lua` + the
  06-12 edit). *Error:* release blocked if the audit drain gate (§2) is not GREEN.

---

## Dependencies & notes

- **§3 depends on §2** (notes author from the *delineated* advanced fork, after the
  split is settled). **§2 depends on §1** (needs all three artifacts). **§1 depends on
  §0** (the skill + contract). **§4 depends on §2 + §3-for-IOSP-readiness** (IOSP
  release needs the merge; the app-note PDFs are this sprint's deliverables but are not
  release-gating IOSP).
- P2AN002 (CORDIC) authoring (#140) is a **separate Math-family track** — does not gate
  this campaign (CORDIC doesn't touch IOSP).
- The fan-out/merge is modeled on the proven `ingest-conductor` + `ingest-wrap-reduce`
  pattern; a dedicated boundary-conductor is a post-proof central-promotion candidate.
