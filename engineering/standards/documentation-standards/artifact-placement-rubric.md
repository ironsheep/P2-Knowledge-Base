# Artifact Placement Rubric — what belongs where, and why

> **Status:** v1 (2026-06-29), authored under the *Capability Coverage &
> App-Note Roster* sprint (Phase 1). Companion to
> `engineering/standards/p2-capability-taxonomy.md` (the *what* — the capability
> spine). This doc is the *form* — given a capability that needs covering, which
> **artifact type** should carry it.

## The four-artifact spectrum

The P2's teaching/reuse artifacts sit on one spectrum of **increasing
pedagogical depth and increasing authorship / trust commitment:**

| Artifact | Pedagogical role | Authored by | Trust tier | What an agent gets |
|---|---|---|---|---|
| **OBEX object** | A reusable *part* — drop it in. No teaching intent. | Community | Community (download-on-demand; not KB-vetted) | Catalog entry + download link |
| **Quick Byte** | A *worked demonstration* of one task; multi-modal; light on *why*. | Parallax | Community/marketing (we route to it) | Catalog entry + modality links (article/video/code) |
| **App note** | *Guided composition* — combining subsystems to solve a recurring task, **with the why**. | **Us** | First-party, validated, KB-trust-stamped | Catalog entry **+ full structured YAML companion** |
| **Manual** | *Systematic reference* for a whole subsystem — complete, canonical. | **Us** | First-party, KB core | Already YAML-backed (the KB *is* the source) |

Two structural facts follow from the "Authored by" column:

- **We can only trust-stamp and serve content we author.** OBEX and Quick Bytes
  we *catalog* (point to); app notes and manuals we *serve* (the content itself
  lives in the KB). This is why an app note earns a YAML companion and a Quick
  Byte does not — see the decision record in
  `engineering/document-production/app-notes/`.
- **Code is linked, not adopted, for community artifacts.** An OBEX object or a
  Quick Byte's source stays at its origin (download-on-demand); we never copy
  community code into the trust-stamped `deliverables/` tree.

## Routing a capability gap to its form

When the coverage analysis surfaces a hole, route it — don't reflexively call
everything an app note:

```
Is the missing thing a reusable COMPONENT (a driver/library to drop in)?
    → OBEX gap → an adoption request (not ours to author).

Is it a single task that just needs to be SHOWN working?
    → Quick Byte gap → suggest to Parallax (we don't author Quick Bytes).

Is it a recurring task needing GUIDED COMPOSITION of subsystems + the why?
    → APP NOTE  ← ours to author; this is what the roster proposes.

Is it a FOUNDATIONAL SUBSYSTEM that's under-documented?
    → MANUAL gap → a chapter/section, not an app note.
```

## The sharp test: app note vs. manual section

The line that's easiest to blur, and the most important to get right:

> **An app note solves a *problem* by composing subsystems.
> A manual section documents a *subsystem* completely.**

- *"Read a temperature sensor over 1-Wire while updating a display"* →
  **app note** (composes E + F + G to solve a task).
- *"Everything the I²C smart-pin mode does"* → **manual section** (documents one
  subsystem, B, exhaustively).

Corollaries:
- If the answer is "document this capability completely and canonically," it's a
  manual, even if it feels app-note-sized.
- If the answer is "show how to *combine* things to get a result," it's an app
  note, even if it touches subsystems the manuals already cover (it *references*
  them, it doesn't re-document them).

## Why this matters for the roster

The coverage matrix will surface gaps **bidirectionally**:
1. **P1-had-it / P2-lacks-it** — classic app-note topics the P1 covered and the
   P2 hasn't.
2. **P2-unique / no-precedent** — capabilities with no P1 analogue (CORDIC,
   streamer, XBYTE, HDMI, USB) that nonetheless need guidance, surfaced from the
   P2 side.

Each gap is then routed through the tree above. The roster's value is not "here
are 30 holes" — it's "here are the holes, **and each one's correct form, with the
reason.**" A hole already filled by a not-yet-indexed artifact (e.g. an existing
OBEX driver) is **not** a gap; the analysis checks against the refreshed corpora,
not stale state.

## See also
- `engineering/standards/p2-capability-taxonomy.md` — the capability spine.
- `engineering/document-production/app-notes/` — the app-note doc class
  (creation guide, voice guide) + the format-donor / companion decision record.
