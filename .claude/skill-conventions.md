# Project skill conventions — P2-Knowledge-Base

This file holds slot values for the central skill set. See
`~/.claude/skills-docs/SKILLS-MAINT.md` for the full schema.

## ⚠️ This is a multi-headed project

P2-Knowledge-Base is **three heads under one repo**, not a single-build app:

1. **KB-for-agents** — the P2KB YAML knowledge base served on demand via
   `p2kb-mcp`. "Green" = valid cross-references, clean index, sourced facts.
   Its build is *validate + regenerate index*. Has its own version.
2. **Source study / ingestion** — studying & ingesting published P2 docs
   (P1 next). **Version-less**: governed by ingestion-quality, cross-ref,
   and audit *gates* plus a completeness *dashboard*, not releases.
3. **Manual production** — the documentation manuals (6+ in flight). Build
   is *PDF generation via PDF Forge* (handback model). **Each manual carries
   its own version + CHANGELOG.**

Consequence for the slot schema (built for a single-headed app): a whole
category of slots — version, plan dir, punch list, release notes, spec —
**has no correct single global value.** Those slots carry a per-head
**routing sentinel** (`<per-head — ...>`) instead of a literal. The sentinel
keeps each skill's Step 0a from hard-stopping (so Step 0b loads the overlay),
and the skill's `project-overlay.md` does the real per-head dispatch:
*identify the head/element, then resolve the artifact from that head's
pattern.* This is the same primitive as `CLAUDE.md`'s Work Type Routing.

---

## Identity

```yaml
USER_NAME:     Stephen
PROJECT_NAME:  P2-Knowledge-Base
```

## Build & test

The one head with an objective local green/red is the **P2KB YAML set**.
`baseline-health` ("are we green") maps to its validators. Manuals build on
PDF Forge (no local gate); ingestion uses quality gates + dashboard.

```yaml
BUILD_COMMAND:          python3 engineering/tools/verify-yaml-format.py
TEST_COMMAND:           python3 engineering/tools/validate-crossref-keys.py
CANONICAL_TEST_TARGET:  local Python validators over the P2KB YAML set (YAML syntax + cross-reference; DoD via validate-dod-release.py)
```

`BUILD_COMMAND` was `validate-yaml-syntax.py` until 2026-08-15. That script scans
only `manifests/` + `engineering/knowledge-base/` and reports "0 files checked /
ALL VALID" for the `deliverables/ai/P2/` content tree — a **hollow green**. The
`baseline-health` overlay had documented the trap for months while the slot kept
naming the trapped command. `verify-yaml-format.py` is the real content-tree
syntax gate.

There is **no automated behavioral test suite** — these validators are the
substitute gate (`baseline-health` §2a). A green here never implies the
documentation is *correct*, only that it parses and resolves.

## Doc audit — the guide layer

The **guide layer** (house voice canon · app-note class guides · each manual's
voice/creation/style guides) has its own gate, added 2026-08-15 by Sprint 1.
It is the layer an author reads *before* writing, so a defect there misdirects
every document downstream. Its file set is globbed, never hand-maintained, and
its exclusions are printed by name.

Five detections: restated voice rule (incl. word blacklists) · the non-existent
`pnut_ts` tool name · dead cited authority paths · codenames · retired-doc
references shown as live.

```yaml
DOC_AUDIT_COMMAND:  python3 engineering/tools/validation/audit-guide-conformance.py --inventory
```

## Build version — PER-HEAD (sentinel)

No global project version. The manual you're working on, or the P2KB YAML
set, owns the version; **ingestion has no version.** Resolved per head.

```yaml
BUILD_VERSION_LOCATION:  <per-head — manual CHANGELOG.md, or P2KB YAML set version; N/A for ingestion; see skill overlay>
BUILD_VERSION_KEY:       <per-head — see skill overlay>
BUILD_VERSION_EXAMPLE:   <per-head — e.g. manual "2.3.0"; see skill overlay>
```

## Doc paths

```yaml
ANALYSIS_DIR:  engineering/analysis/

# PER-HEAD (sentinel) — resolved by Work Type Routing / skill overlay:
PLAN_DIR:           engineering/planning/   # SINGLE dir for ALL engineering heads (decided 2026-06-11 — unify; supersedes the per-head sentinel). Stragglers in operations/planning + operations/sprints migrate here (separable cleanup). Archive stays PLAN_ARCHIVE_DIR.
PLAN_ARCHIVE_DIR:   engineering/history/sprints/
PUNCH_LIST_DOC:     <per-head — one per manual, per ingestion source, and for the P2KB YAML set; P2KB-CORRECTION-FINDINGS.md is the YAML-set register; see skill overlay>
RELEASE_NOTES_DOC:  <per-head — manual CHANGELOG, or P2KB YAML release notes; N/A for ingestion (uses completeness dashboard); see skill overlay>
SPEC_DOC:           <per-head — N/A for ingestion; see skill overlay>
```

## Execution environments — the two-environment split

This project shares one working tree across two environments (central v7
vocabulary). Everything authored here; three classes of verdict are not
observable here at all.

```yaml
EXEC_ENV_LIMITED:    the dev container — authors and edits every artifact; runs the Python
                     validators, the guide-conformance instrument, and the PDF-tooling chain;
                     compiles Spin2/PASM2 with `pnut-ts` (add `-d` for DEBUG code). Has NO GUI,
                     NO P2 silicon, and NO PDF renderer (local Pandoc is 1.19 and off-limits).
EXEC_ENV_CANONICAL:  Stephen's host — (1) PDF Forge renders every manual PDF; (2) real P2
                     silicon runs the hardware-verification tests behind the empirical ledger;
                     (3) the DEBUG display windows render there and come back as BMP captures.
```

Applying the three rules here: a missing renderer or absent P2 board in the
container is **the shape of the project, never a defect** — do not engineer
around it. **Stopping at the outbound bundle is a complete outcome**
(`prepare-manual` is designed to end there). And a **clean compile or a clean
Forge log is provisional**: it proves legality and exit-0, never semantics and
never that the page rendered — the PDF that comes back must be *looked at*.

## Domain authority

```yaml
DOMAIN_AUTHORITY:  the ingested primary sources under `engineering/ingestion/`, in this
                   precedence order: (1) empirical / hardware-verified results in
                   `engineering/ingestion/external-sources/hardware-verification/`
                   (P2-EMPIRICAL-FINDINGS.md) — strongest, and has overturned every other
                   tier; (2) the `pnut-ts` compiler's actual behavior, for legality only;
                   (3) Parallax documentary sources (Propeller 2 Documentation v35 Rev B/C,
                   Spin2 v55 release notes) under `engineering/ingestion/sources/`;
                   (4) the published P2KB YAML set. Community/forum/Titus material is an
                   UPSTREAM LEAD, never a citable authority.
```

**`p2kb-mcp` is deliberately NOT the authority here.** It serves what *this
project publishes*, so citing it inside this project is circular — it is the
authority for every *other* project's P2 questions, not for ours. Ours is the
ingestion tree the YAML was built from. Likewise, one P2 manual or app note is
never authority for another (they are peer derivations).

## Who the deliverable serves — per head

```yaml
DELIVERABLE_AUDIENCE:  manual / app-note / guide  -> human-reader
                       P2KB YAML set (deliverables/ai/P2/, served via p2kb-mcp) -> agent-consumer
                       ingestion artifacts (feed the YAML set) -> agent-consumer
                       OBEX + Quick Bytes integration records  -> agent-consumer
                       example corpora + verification .spin2   -> code-user
```

The **agent-consumer bar is the strict one and it governs the KB heads**: cite
the authority or **omit the entry** — an entry shipped marked-unverified is a
defect wearing a caveat, because a remote agent cannot weigh a hedge and a wrong
fact becomes silently authoritative in generated code. This is the same rule the
project already ran under its own names (no inference or derivation in YAML; no
unsourced claims); the slot is what makes it apply automatically at the
`document-finalize` and `sprint-closeout` gates.

## Conformance guides

Replaces the retired `STYLE_GUIDE_DOC` / `HELP_VOICING_GUIDE` /
`MANUAL_VOICING_GUIDE` slots (central v8). The guide layer this maps was
normalized and gated by Sprint 1 (2026-08-15) — three layers: house canon →
class guide → per-document guide, with the document layer declaring
ADOPT/ADAPT/REJECT per rule.

```yaml
CONFORMANCE_GUIDES:
  - surface:  any manual / guide prose (opus-master)
    guide:    engineering/standards/documentation-standards/documentation-voices-catalog.md
              (house canon — sole home of rules R1–R4), THEN the element's own
              engineering/document-production/manuals/<slug>/voice-guide.md
    when:     read before authoring into the surface; re-read at finalize
    strength: reference

  - surface:  app notes
    guide:    engineering/standards/documentation-standards/APP-NOTE-VOICE-GUIDE.md
              (class layer), THEN the app note's own voice-guide.md
    when:     read before authoring
    strength: reference

  - surface:  the guide layer itself (voice/creation/style guides, MANUAL-DESCRIPTORs)
    guide:    documentation-voices-catalog.md R1–R4
    when:     any edit to a guide
    strength: gate      # DOC_AUDIT_COMMAND is the instrument; must read 0 findings

  - surface:  every CHANGELOG.md (manuals, app notes, the P2KB YAML set, repo root)
    guide:    central:changelog-voicing        # mode: Released · class: 3 (Published document)
    when:     before writing any changelog entry
    strength: reference
    note:     ADOPTION INCOMPLETE — central's Class 3 profile is an unauthored stub
              ("to be authored when a manual release calls for it"). The shared core
              (§1–§4) governs now; the project's local
              engineering/document-production/methodology/changelog-style-guide.md is
              RETAINED as the Class 3 taxonomy until that profile is authored upstream.
              Tracked as a task; do NOT delete the local guide before then.

  - surface:  authored .spin2 source (verification tests, utility objects)
    guide:    central:spin2-authoring-guide
    when:     before writing or editing any .spin2 file
    strength: gate
    note:     ARMED 2026-08-22 by `audit-spin2-ascii.py` (see STYLE_GATE_COMMAND below),
              which enforces §1.1 mechanically over the authored corpus and reports each
              violation's CONTEXT, because that is what sets its severity:
                • debug() payload / string literal -> RUNTIME. A codepoint above 127 goes
                  out the debug link as multi-byte UTF-8: the terminal can take the stream
                  as BINARY rather than ASCII, mis-render, or act on an escape nobody sent.
                  Expected output is destroyed and NOTHING in the build says so.
                • code -> compile / semantics.
                • comment -> portability (the reader's own editor) + byte-identity with
                  the printed block.
              **Non-ASCII is acceptable ONLY in a comment**, and the box-drawing exception
              (U+2500-257F / U+2580-259F) is a comment-only exception. **Inside `debug(...)`
              nothing is a comment** — text that merely LOOKS like commentary is payload and
              is transmitted ({{USER_NAME}}, 2026-08-22).
              `pnut-ts` exiting 0 proves NONE of this; it proves the file parsed. An earlier
              draft of this note read the compile result as evidence that the comment clause
              was "portability, not compile-break" — that inverted the guide and is wrong:
              the guide's "silent corruption" wording is about the runtime, where it is
              exactly right. §1.1's other rules remain unenforced pending further work.

  - surface:  manual/app-note EXAMPLE CORPORA (examples-library/*.spin2)
    guide:    central:spin2-authoring-guide, with §4.2 (file header) and §4.2.1
              (licence footer) satisfied by GENERATION, not by hand
    when:     before writing or editing any example file
    strength: gate
    note:     RESOLVED 2026-08-18. These files are byte-identical to the listing
              printed in their document, so a hand-written header cannot exist in
              them — the two requirements were jointly impossible and the whole
              fleet silently ran without headers. `engineering/tools/sync-manual-
              examples.py` now generates the header and footer, and the identity
              gate asserts the file BODY against the printed block. Everything
              except `Purpose` is derived, so nothing drifts; `Purpose` lives in
              each corpus's PURPOSES.md. §1.1 (ASCII) applies to the generated
              header too — the tool transliterates derived text and refuses what
              it cannot map. §2.1 (no single-letter names) yields to cross-chapter
              continuity where a later chapter grows an earlier chapter's program.
              ADOPTION IS PER-DOCUMENT, at that document's next release: adopted
              documents are gated hard, un-adopted ones report INFO and pass.

STYLE_GATE_COMMAND:  python3 engineering/tools/validation/audit-spin2-ascii.py
```

**Never copy a `central:` guide into this repo** — a copy is a fork. The one
`SPIN2-AUTHORING-GUIDE.md` under `engineering/ingestion/external-inputs/` is a
*received* external artifact inside an ingestion handoff package, not a project
guide; it stays where it is as part of that record.

## Promotion role

P2-Knowledge-Base is a **promotion source** — the origin of the
`overlay-survey` → `fleet-skill-survey` → central-promotion pipeline. Its
`sprint-retrospective` therefore keeps candidate-buffer entries through an
**adopt → certify → promote** window (central §5's promotion-source verdicts),
rather than deleting them the moment they're addressed. Adopted 2026-07-24
during the v1→v3 overlay reconcile (central v2 absorbed the lifecycle natively;
this slot selects it).

```yaml
PROMOTION_SOURCE: yes
```

## Audience & vocabulary

```yaml
RELEASE_NOTES_AUDIENCE:  the P2 developer community
```

## Document finalize

`DOC_RENDER_COMMAND` is intentionally **omitted** — manuals render on PDF
Forge (handback model), so `document-finalize` hands the document back for
the user to render rather than running a local render command.

---

## Omitted slots (intentional)

- **P2 development cycle** — omitted entirely. The repo holds ~2000 `.spin2`
  files, but they are examples / OBEX objects, not one firmware project with
  a single top file. `p2-dev-cycle` is not part of this project's workflow.
- **Filename patterns** — omitted; central defaults apply (per-head plan
  naming is designed in overlays).
- **Voicing / style guides** (`MANUAL_VOICING_GUIDE`, `STYLE_GUIDE_DOC`,
  `HELP_VOICING_GUIDE`) — **retired by central v8**; converted to
  `CONFORMANCE_GUIDES` rows above, which is what the three-differently-voiced-
  surfaces shape needed all along.
- **Model strategy** (`MODEL_TIERS`, `DEFAULT_MODEL`) — removed with the
  `model-strategy` skill's retirement (central v8). Model choice is now an
  optional one-line `recommended model:` annotation in `plan-to-tasks` §2.
  CLAUDE.md's own model table remains as project guidance.
- **`P2_DEBUG_BAUD`** — N/A. `p2-dev-cycle` is not part of this project's
  workflow (see above), so v8's `-b` toolchain-conditional re-check does not
  apply: no wrapper or template here downloads to a P2.
- **Per-task detail artifacts**, `PROJECT_INIT_DATE`, `TEST_FLEET_DESCRIPTION`
  — omitted; defaults apply.

## Known cleanup debt (separable tasks — not bootstrap work)

1. Consolidate scattered plan dirs (`engineering/operations/sprints`,
   `engineering/operations/planning`, `engineering/planning`).
2. Relocate punch-list content to its correct per-head homes.
3. Give `engineering/operations/P2KB-CORRECTION-FINDINGS.md` the
   `punch-list-maintenance` lifecycle (complete → dated archive; latest copy
   holds only outstanding work).
