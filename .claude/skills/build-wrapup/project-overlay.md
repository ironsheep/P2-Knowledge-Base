# P2-Knowledge-Base overlay — build-wrapup

> **Status (2026-06-22).** The Work Type Routing model is adopted (multi-head
> dispatch + `whats-next` front door). Still open: the **YAML head's version /
> release-notes homes are `TBD`** in `HEAD-DISPATCH-DRAFT.md` — resolve with
> {{USER_NAME}} when a YAML-head wrap-up needs them.

## Augments Step 0a — resolving per-head `BUILD_VERSION_*` and `RELEASE_NOTES_DOC`

Both version and release-notes are per-head routing sentinels. There is no
global build version. Identify the head/element, then resolve from
`.claude/skills/HEAD-DISPATCH-DRAFT.md`:

- **MANUAL** — version + release notes are the manual's own `CHANGELOG.md`
  (the audience-facing summary lands there); also reflected in the
  `deliverables/documents/README.md` version line. The project-baked
  `release-manual` / `audit-changelog` skills own the release mechanics —
  defer to them for *when* an entry is written and how it is audited, and to
  the guide below for *how it is worded*.
- **YAML (KB)** — the P2KB YAML set's own version + release notes
  (homes `TBD`).
- **INGESTION** — **not applicable.** Ingestion is version-less and has no
  release notes; it reports against quality/cross-ref/audit gates and the
  completeness dashboard instead. On the ingestion head, `build-wrapup`
  should say so rather than invent a version/notes entry.

`RELEASE_NOTES_AUDIENCE` is "the P2 developer community" for manual and
YAML release notes.

## Augments §3 — this project's two changelog coordinates

Central §3 now carries the partial-coverage rule itself (read both rows; the
shared core governs voice, the local profile governs shape). Only the project's
own coordinates are left here:

- **Class 3 — Published document**, for every manual and app-note `CHANGELOG.md`.
- **Mode: Released** for every element already in `deliverables/documents/`;
  **Mode: Development** until an element's first public release.
  **`PUBLICATION-ROSTER.md`'s status section is what decides which** — do not
  infer the mode from whether a CHANGELOG already has entries.

**One live gap while the trim is owed.** The local class-3 profile predates
central §1.5 and is silent on the mandatory **theme line**, so an author who
reads only the profile will omit it. Write one under every version heading.
*This note expires when the profile is trimmed to central's complement* — after
which the profile carries no voice rules at all and §1.5 is the only source.
