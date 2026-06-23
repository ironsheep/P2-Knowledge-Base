# P2 Architect's Guide — First-Draft Build · Sprint Plan

**Status:** ✅ **SPRINT COMPLETE — v0.1.0 first draft** (closed out 2026-06-23). All 7 sprint tasks
(#93–#99) done. The draft EXCEEDED the original 3-chapter DoD: a 4th chapter — **Ch2 "Reading P2
Code"** — was added mid-sprint for readers with no P1/Spin2/PASM2 background (PLANNING D2), plus the
figure pass (5 figures) and an edition cross-check against Propeller Manual v1.0. Production PDF
generated clean on the Forge (48pp). Parked/follow-ups live in PLANNING §15 + PUNCH-LIST + gap G-P1-007.
Next: a review pass, then `release-manual` when ready.

_(original planning header)_ rich-planning phase · 2026-06-22 · head **manual** · element `p2-architect-guide`
**Goal (DoD):** a **first-draft PDF in hand** — the manual generated through PDF Forge, verified
complete (page count / outline / sections / cover / code rendering / callouts), defects logged.
**Charter (spec):** `engineering/document-production/manuals/p2-architect-guide/PLANNING.md` +
`creation-guide.md` + `voice-guide.md` (already authored & committed — this sprint *executes* them).

> **This plan does not re-decide the manual.** Identity, scope, chapter architecture, voice, source
> map, and decisions D1–D6 are locked in the charter. This plan sequences the **build to first draft**
> and resolves the **production-mechanics** decisions (DD1–DD5) the charter deferred.

---

## Baseline (manual head — no local build gate)

Manuals render on PDF Forge (handback), so there is no compiler green/red. The entry baseline is the
**document state**, and it is **greenfield**: the manual has a charter + creation-guide + voice-guide,
but **no `opus-master/`, no `workspace/`, no `outbound/`** yet. The exit assertion compares like with
like: a first-draft PDF exists, is verified structurally complete, and its open defects are captured in
the manual's `PUNCH-LIST.md` (not silently carried). No prior version to regress.

### Entry checks — recorded at sprint-start (2026-06-22)

- **Build number (§1):** **v0.1.0** ("first draft"), per DD4 — created in `CHANGELOG.md` + `request.json`
  metadata during scaffolding («#93»). The manual owns its own version (manual head).
- **Working-tree audit (§2):** clean for this sprint. Branch `main` (no-branching rule). Only untracked
  file in the blast radius is this plan doc (commits with the work). One unrelated pre-existing untracked
  file — `engineering/ingestion/sources/silicon-doc/…v35 - Rev B_C Silicon.docx` (ingestion head) — is
  out of scope and left in place. No uncommitted edits to any file this sprint touches.
- **Tracking-readiness (§3):** **READY.** 29 completed tasks archived; board carries the 7
  `arch-guide-v0.1` tasks + paused other-head work. Noted (non-blocking): 62 `checkpoint_*` context
  snapshots accumulated (most superseded historical sprint-state) — a separable context-prune sweep, not
  a gate.
- **Baseline-health (§4):** N/A as a compiler gate (manual head — no local build). Entry baseline =
  the greenfield document state above. The YAML head (unrelated) last shipped green at v1.10.1; not this
  sprint's exit comparator.

---

## Design decisions — ALL RESOLVED (Stephen, 2026-06-22)

DD1–DD5 confirmed as recommended. The questions pass is empty; the plan has cleared its exit gate.

- **DD1 — "P1 note:" sidebar mechanism.** The charter weaves P1→P2 migration as `P1 note:` sidebars
  (D3). The shared platform `content.sty` has no such environment. **Recommend:** a thin **local**
  filter `filters/p2kb-architect-local.lua` mapping a `::: p1note` fenced div → a `P1NoteBlock`
  tcolorbox defined in `templates/p2kb-architect-local.sty`, registered in `request.json` *after* the
  shared `p2kb-platform-*` filters. Keeps the shared platform pristine; the sidebar is the one
  architect-specific skin. *(Rejected: reusing `TipBlock` — semantically muddy; editing the shared
  platform filter — pollutes every manual with an architect-only class.)*
- **DD2 — Platform-max, thin local overlay.** Local files named `p2kb-architect-*`: `reference.latex`
  (thin entry), `local.sty` (skin + `P1NoteBlock`), `diagrams.sty` (TikZ stub, inert). Ride the
  **shared** `p2kb-platform-{foundation,content}.sty` and the **shared** `p2kb-platform-*` lua filters
  (figures, tables, mnemonic-bold, code-coloring, pagination) — exactly the Streamer-pilot shape.
  **Recommend:** accept (this is the already-approved "ride the shared platform" direction; the
  architect guide becomes the cleanest born-on-platform exemplar).
- **DD3 — Body file shape.** **Recommend:** single `opus-master/architect-guide-body.md` (Ch1–3 +
  appendices + glossary + where-to-next) plus a separate `opus-master/front-matter.md`, assembled by
  `assemble-manual.sh` — matches Streamer. (A slim 3-chapter book doesn't warrant per-chapter files.)
- **DD4 — Version & metadata.** **Recommend:** start at **v0.1.0** ("first draft") in `request.json`
  metadata and a new `CHANGELOG.md`; title/subtitle/author per charter D1 (*The P2 Architect's Guide —
  Thinking in Cogs, Pins, and Forces*; author *Iron Sheep Productions, LLC*).
- **DD5 — Diagrams deferred to a later visual pass.** Ch1's mental model benefits from figures, but
  authoring diagrams is its own effort. **Recommend:** first draft is **prose-complete**, ships with
  `diagrams.sty` as an inert TikZ stub (like Streamer), and marks intended figure locations as
  `> **[Figure — …]**` placeholders logged to `PUNCH-LIST.md` for a post-first-draft visual pass.
  This keeps the DoD (first-draft PDF) reachable without a diagram sub-project.

---

## 1. Scaffold the workspace + opus-master skeleton (the brand-new-manual setup)

**Why.** Nothing can be authored or rendered until the manual has the canonical
`opus-master/` source and a `workspace/` production stack. This section also *verifies the
brand-new-manual setup process* (charter §13; task #93) — the first time we stand a manual up directly
on the unified platform.

**Starting point (greenfield).** `manuals/p2-architect-guide/` holds only the three planning `.md`s.
`workspace/p2-architect-guide/` and `outbound/p2-architect-guide/` do **not** exist. Template source:
`engineering/document-production/workspace/p2-streamer-programming-guide/` (`README.md`,
`assemble-manual.sh`, `request.json`, `templates/p2kb-streamer-{reference.latex,local.sty,diagrams.sty}`,
`assets/book-artwork.png`).

**Target.** Create:
- `manuals/p2-architect-guide/opus-master/front-matter.md` (skeleton — filled in §2) and
  `opus-master/architect-guide-body.md` (skeleton with the Ch1–3 + appendix + glossary headings).
- `manuals/p2-architect-guide/CHANGELOG.md` (v0.1.0 stub — DD4).
- `workspace/p2-architect-guide/`:
  - `assemble-manual.sh` — cloned from Streamer, repointed to `architect-guide` paths + body filename.
  - `request.json` — template `p2kb-architect-reference`; lua_filters = the five shared `p2kb-platform-*`
    **plus** `p2kb-architect-local` (DD1); metadata per DD4; pandoc_args identical to Streamer
    (`--top-level-division=chapter`, `--pdf-engine=xelatex`, `--toc`, `--toc-depth=2`).
  - `templates/p2kb-architect-reference.latex` — clone of Streamer's, renamed `\usepackage`s:
    loads `p2kb-platform-foundation`, `p2kb-platform-content`, `p2kb-architect-local`,
    `p2kb-architect-diagrams`.
  - `templates/p2kb-architect-local.sty` — thin skin; **adds `P1NoteBlock`** (DD1).
  - `templates/p2kb-architect-diagrams.sty` — TikZ stub (inert; DD5).
  - `filters/p2kb-architect-local.lua` — maps `::: p1note` → `P1NoteBlock` (DD1).
  - `assets/book-artwork.png` — copy the shared cover (verify md5 matches the shared one per
    `reference_shared_manual_cover_artwork`).
  - `README.md` + `PUNCH-LIST.md` — cloned/adapted from Streamer.

**Integration points.** Shared `platform/` filters + `.sty` are referenced by name in `request.json`
and `*-reference.latex`; the Forge stage step (§7) stages them from `platform/`. The shared cover is
referenced by `assets/book-artwork.png`.

**Verification (normal / edge / error).**
- *Normal:* `bash assemble-manual.sh` runs clean and emits `P2-Architect-Guide.md` from the two
  skeleton files.
- *Edge:* skeleton body with one `::: p1note` and one ```spin2 fence assembles without error.
- *Error:* a missing source file makes `assemble-manual.sh` exit non-zero with the named-file message
  (inherited from the Streamer script's guard) — confirm it still fires after repointing.
- Confirm `book-artwork.png` md5 == shared cover; confirm roster row updated from "planning" toward
  "in development (workspace stood up)".

## 2. Front matter (house standard)

**Why.** The house front-matter standard
(`engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`) gives
every manual a consistent banner, title page, organization panel, copyright, how-to-use, and
conventions block; it is prepended to the body at assembly.

**Starting point.** `manuals/p2-streamer-programming-guide/opus-master/front-matter.md` (the reference
implementation, incl. `{=latex}` raw blocks for the title page).

**Target.** `opus-master/front-matter.md` for the Architect's Guide: banner + title page (charter D1
title/subtitle), organization/author panel, copyright, **how-to-use = the four reading paths**
(newcomer / P1-vet / working-dev / agent — charter §5 + creation-guide §3.5), and a conventions block
(COG-not-CPU, code-constants, the `P1 note:` sidebar, the five-color code system).

**Verification.** Renders as the first pages of the PDF with correct cover image, title, and a
readable reading-paths table; conventions block matches what the body actually uses.

## 3. Chapter 1 — "Meet the Propeller 2"

**Why.** The warm, feature-first mental model (charter §5, creation-guide §5.1). Concrete, no spatial
abstraction; quietly seeds "each cog just keeps running, independently" for Ch3 to cash in.

**Sources (trust chain — nothing invented).** `deliverables/ai/P2/architecture/` —
`p2-architecture-mental-model.yaml` (the AI-facing half, already written), `cog.yaml`, `hub.yaml`,
`cordic.yaml`, `streamer/`, `event_system.yaml`, `interrupts.yaml`, `clock_system.yaml`, `boot-rom/`,
`locks.yaml`, `lookup_ram.yaml`, `fifo.yaml`, `xbyte_engine.yaml`; Silicon Doc v35; P2 datasheet.
Front-matter MCU↔FPGA *hook* (accessible, no abstraction) lands here per charter §5.1.

**PRIOR-ART PROSE — the PASM2 Manual's Part I (harmonize + link-out, never duplicate).** The
P2 Assembly Language Manual already carries six prose orientation chapters in
`manuals/p2-assembly-language-manual/opus-master/part-i/` — esp. `chapter-01-execution-model.md`
(8-COG architecture, COG/LUT/hub memory, pipeline, exec modes), `chapter-04-timing.md` (clock, hub
rotation, determinism), `chapter-05-hardware.md` (CORDIC, Smart Pins, Streamer, Events/Interrupts).
This is the *same subsystems at a different altitude* (assembly-programmer execution model vs. our warm
feature-first mental model) — exactly one of the scattered orientation pockets this guide unifies
(charter origin / §2). Treat it as: (a) **prior-art to mine** so Ch1 reuses verified framings + matches
terminology — both derive from the same YAML + Silicon Doc, so any divergence is a **defect to
reconcile, not a stylistic choice**; (b) the **link-out target** for assembly-level depth (pipeline
cycles, exec-mode switching, hub timing) — Ch1 orients and points there, never rewrites it.

**Target.** Feature tour (8 cogs · pins · hub · smart pins · CORDIC · streamer/FIFO · events ·
memory/boot · clock), each "what it does + why it's nice," orient-then-link-out. Woven `::: p1note`
sidebars (same: 8 cogs / hub / locks). Any code is ```spin2/```pasm2-fenced and **pnut_ts-verified**.

**Verification.** Every capability claim traces to a cited source YAML / Silicon Doc / datasheet
(creation-guide §4.4 protocol); no enumeration that duplicates a reference manual (link-out instead);
*edge:* a P1-vet can read the sidebars as a standalone delta; *error/anti-case:* no abstraction has
leaked in (the comfort-first gate, charter §12). Code examples compile under `pnut_ts`.

## 4. Chapter 2 — "Putting It to Work"

**Why.** Use the features; build comfort through doing (charter §5, creation-guide §5.2).

**Sources.** `deliverables/ai/P2/guides/spin2-getting-started.yaml`, `pasm2-getting-started.yaml`;
`serial_loader.yaml` / `boot-rom/`; `deliverables/ai/P2/language/` YAML. **Prior-art / link-out:** the
PASM2 Manual's `part-i/chapter-01-execution-model.md` (COG/LUT/hub-exec modes, starting/stopping cogs)
and `chapter-06-address-modes.md` — harmonize the cog/object/run-time framing with them, and link out
there for the assembly-level execution detail rather than restating it.

**Target.** Launch a cog; drive a pin; the Spin2-vs-PASM2 *decision* (not a tutorial); the
object/run-time model; hub sharing; boot/run. Short, **pnut_ts-verified** examples; link out to Spin2
v55 / PASM2 manual / Smart Pins / Streamer guides for depth. Woven `::: p1note` sidebars (changed: hub
egg-beater, clock setup, 64 pins).

**Verification.** Each example compiles under `pnut_ts`; each "for more, see …" points at a real
manual; *anti-case:* no passage drifts into being a Spin2 reference (link-out contract, charter §2/§12);
still comfort-register (voice-guide §10.2).

## 5. Chapter 3 — "Thinking in P2 (Functional Decomposition)"

**Why.** The earned capstone (charter §5, creation-guide §5.3). The space-vs-time thesis + the forces +
the first-contact procedure + ONE worked derivation. **Teaches the METHOD, never prescribes an
outcome** (the load-bearing anti-prescription principle, charter §5/§7/§12).

**Sources (golden home — Ch3 derives, never drifts; charter §7).** `deliverables/ai/P2/architecture/
decomposition/` — all 12 entries (`decomposition-method`, `first-contact-procedure`,
`resource-ownership`, `data-flow-contracts`, `rate-adaptation`, `altitude-layering`,
`cross-cutting-forces`, `resource-budget`, `spatial-computing`, `evaluation-vocabulary`,
`decomposition-glossary`, `worked-derivation-robot-dog`).

**Target.** Formal space/time thesis as the rationale → the forces → the first-contact procedure → the
**robot-dog derivation as a DEMONSTRATION** explicitly framed as one machine's answer (not a template).
Warmth stays, rigor rises, glibness → 0 (voice-guide §10.2). Anti-prescription **gate applied to every
section**.

**Verification (the gravest-risk chapter).** Every claim is supported by the decomposition YAML — any
gap is routed to corrections/gaps, **not** asserted (charter §7); **anti-prescription gate:** each
section teaches a *technique for deriving*, and the robot dog stays labeled as one machine's answer
(*error/anti-case:* any "do it this way" phrasing or template-reading robot-dog is a defect to fix
before sign-off); any authoring-time improvement to the theory lands in the YAML **first**, then renders
here.

## 6. Back matter — appendices, glossary, where-to-next

**Why.** Charter §5/§5.1/§5.2 + creation-guide §5.5/§5.6.

**Target.**
- **Appendix A — Computing in Space and Time (Why We Borrow FPGA Language):** temporal→spatial spectrum;
  honest *what-transfers / what-doesn't* (coarse-grained, still software, no place-and-route); the
  **FPGA-terminology table** (term · FPGA meaning · P2 mapping · where it's loose). Source:
  `architecture/decomposition/spatial-computing.yaml`.
- **Appendix B — Further Reading on Functional Decomposition:** two axes (logical: Parnas, Constantine
  & Yourdon, Page-Jones; physical/concurrent: Hoare CSP + transputer/Occam, optional Kung systolic),
  each with a one-line "why it's relevant to P2." Sources cited in `decomposition-method.yaml`.
- **Glossary** from `decomposition-glossary.yaml`; **where-to-next** map into the reference manuals.

**Verification.** *Appendix A anti-case:* no sentence implies the P2 *is* an FPGA (the
what-doesn't column is the guard, charter §12). *Appendix B:* **every** author/title/year is
**verified before publish** — marked `NEEDS-VERIFICATION` until checked (charter §12); a short correct
list beats an impressive wrong one. Glossary terms match the YAML; where-to-next links resolve to real
manuals.

## 7. Prepare → first Forge build → first-draft review (DoD)

**Why.** Produce the first-draft PDF in hand and verify it — the sprint's reason for being.

**Steps.**
1. `prepare-manual` — runs `assemble-manual.sh` (front-matter + body → `P2-Architect-Guide.md`) +
   `latex-escape-all.sh`, then stages **changed files only** to `outbound/p2-architect-guide/`
   (first build: the assembled `.md`, `request.json`, the local templates/filters, and any shared
   platform files the manual store lacks — judged per
   `feedback_no_restage_unchanged_after_manual_pdf` / `feedback_manual_store_independent_of_interactive`).
2. **Stephen deploys to PDF Forge; Forge generates** (handback — I do not run Forge,
   `reference_no_gui_in_container` / `reference_pdf_forge_interaction_model`).
3. **Verify the returned PDF myself** (`release-manual`'s completeness checks, applied as a *review* not
   a release): page count plausible, outline/TOC present with Ch1–3 + appendices, cover image + title
   page correct, code blocks colored (spin2 blue / pasm2 green), `::: p1note` sidebars render as boxes,
   no silent content drop — **read `output/<doc>.compile.log`** (guards against the 100%-success
   silent-drop trap, `reference_forge_silent_content_drop`).

**Verification (normal / edge / error).** *Normal:* PDF opens, all sections present.
*Edge:* a long code listing and a `p1note` near a page break paginate without overflow.
*Error:* if the compile log shows a recovered error (figure-in-figure, missing glyph, undefined box),
log it to `PUNCH-LIST.md` and fix the root cause before declaring the draft done — defects are not
carried (CLAUDE.md quality philosophy). Emoji/marker glyphs confirmed to render (or logged for the
visual pass).

---

## Verification protocol (applies to all authoring sections)

Inherited from `creation-guide.md §4.4` — every claim traces to a cited primary source (architecture /
language / decomposition YAML · Silicon Doc v35 · datasheet); red-flag phrases ("also provides", "side
effect", "automatically", "eliminates") trigger re-verification; code is ```fence-tagged and
**pnut_ts-verified**; Ch3 additionally passes the **anti-prescription gate**; Appendix B citations are
**verified before publish**. COG-not-CPU; code constants not arithmetic values; link-out never
duplicate.

## Out of scope (named carve-outs — not silent deferrals)

- **Diagram authoring** (DD5) — first draft is prose-complete with figure placeholders; the visual/
  diagram pass is a follow-on once the draft is reviewed.
- **The AI-facing YAML sibling** (charter §8 / D4) — the decomposition + mental-model YAML already
  exist as the agent-facing form; *new* YAML shaping for dual-target parity is a separate effort, not
  part of getting the human first draft in hand.
- **Public release** (`release-manual` → deliverables, roster Live promotion) — this sprint ends at a
  *reviewed first draft*; promotion to Live is a later decision after Stephen reads it.
- **Full cross-manual intro survey** — beyond the PASM2 Part I prior-art folded into Ch1/Ch2 (§3/§4),
  the other manuals' orientation prose (Smart Pins tutorial, Streamer guide, Debug manual) is also
  prior-art worth harmonizing against; the first draft mines PASM2 Part I (richest overlap) and treats a
  full survey as a light follow-on.
- **Reframing PASM2 Part I downward** — once this guide is the orientation layer, whether the PASM2
  Manual's Part I should later *shrink* its architecture orientation and link *up* to this guide is a
  cross-manual question raised, not resolved, here.

---

## Section ↔ task cross-reference (sprint tag `arch-guide-v0.1`)

`todo_next tags:["arch-guide-v0.1"]` walks these in **execution order** (the rework-safe order, not the
plan's section numbering — front matter is authored late so its conventions block reflects what the
chapters actually use; it only documents conventions the scaffolding already fixed):

| Plan § | Deliverable | Task | Exec order | Est |
| ------ | ----------- | ---- | ---------- | --- |
| §1 | Scaffold workspace + opus-master skeleton (brand-new-manual setup) | «#93» | 1 | 90m |
| §3 | Ch1 — Meet the Propeller 2 | «#94» | 2 | 120m |
| §4 | Ch2 — Putting It to Work | «#95» | 3 | 120m |
| §5 | Ch3 — Thinking in P2 (Functional Decomposition) | «#96» | 4 | 150m |
| §6 | Back matter — Appendix A/B, glossary, where-to-next | «#97» | 5 | 90m |
| §2 | Front matter (house standard) | «#98» | 6 | 60m |
| §7 | Prepare → first Forge build → first-draft review (DoD) | «#99» | 7 | 75m |

Total effort ≈ 11.75h. All seven tasks tagged `arch-guide-v0.1` (queryable as a unit) + `manual` +
`p2-architect-guide`.
