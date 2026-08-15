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

## Augments §3 — changelog class profile and mode

Central §3 reads the changelog's `CONFORMANCE_GUIDES` row, which names
`central:changelog-voicing`. This project's coordinates in that guide's two axes:

- **Class 3 — Published document**, for every manual and app-note `CHANGELOG.md`.
  Part-based taxonomy; entries lead with the instruction, directive, or
  component; the full prior-state ban including "no longer."
- **Mode: Released**, for every element already in `deliverables/documents/`.
  An element still in development is Mode: Development until its first public
  release, and the roster's status section is what decides which.

**Adoption is incomplete and the gap is upstream, not here.** Central's Class 3
profile is an unauthored stub. Until it is written, the guide's shared core
(§1–§4) governs voice and the project's own
`engineering/document-production/methodology/changelog-style-guide.md` supplies
the Class 3 taxonomy — the section structure, entry formats, and length budgets.
That local file is **retained deliberately**, not by oversight; do not delete it
as a redundant copy. It is also the natural source text for the upstream Class 3
profile.

**Heading form is already aligned** — the local guide and central §1.5 both
mandate `## vX.Y.Z (YYYY-MM-DD)`, so §7.1's silent-reader-breakage risk does not
apply to this project's existing readers. What central adds that the local guide
does not is the mandatory **theme line** under the heading as the
machine-readable release summary; write one on every entry.
