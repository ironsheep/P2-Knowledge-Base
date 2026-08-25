# P2-Knowledge-Base overlay — build-wrapup

> **Status (2026-08-25).** The Work Type Routing model is adopted (multi-head
> dispatch + `whats-next` front door). The **YAML head's version / release-notes
> homes are resolved** in `HEAD-DISPATCH-DRAFT.md`: version = the latest git tag
> (mirrored by the top-level `README.md` badge + top-level `CHANGELOG.md`);
> release notes = the repo-root `CHANGELOG.md` (what `release-yamls` §4 writes);
> `deliverables/ai/P2/CHANGELOG.md` is a co-located POINTER holding no entries. That split is
> reader-facing home co-located with the served content — `release-yamls` Step 4
> has not yet been updated to write to it, so keep it in sync with the top-level
> `CHANGELOG.md` by hand until that skill is.

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
- **YAML (KB)** — version = the latest git tag; release notes =
  the repo-root `CHANGELOG.md` (the record), reachable from the served content via its pointer (co-located with the served
  content). The top-level `CHANGELOG.md` remains the engineering-repo record
  `release-yamls` writes to — the two are not yet wired together, so reconcile
  by hand until that skill is updated.
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

- **Class 3 — Published document**, for every manual and app-note `CHANGELOG.md`,
  and for the repo-root `CHANGELOG.md` (the YAML set's record).
- **Mode: Released** for every element already in `deliverables/documents/`, and
  for the YAML set (already published, consumed by every `p2kb-mcp` client);
  **Mode: Development** until an element's first public release.
  **`PUBLICATION-ROSTER.md`'s status section is what decides which** for
  manuals/app-notes — do not infer the mode from whether a CHANGELOG already has
  entries. The YAML set has no roster row; it is released the day it first ships
  a git tag, which it already has.

**One live gap while the trim is owed.** The local class-3 profile predates
central §1.5 and is silent on the mandatory **theme line**, so an author who
reads only the profile will omit it. Write one under every version heading.
*This note expires when the profile is trimmed to central's complement* — after
which the profile carries no voice rules at all and §1.5 is the only source.
