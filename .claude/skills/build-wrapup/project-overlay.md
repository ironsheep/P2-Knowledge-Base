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
  `release-manual` / `audit-changelog` skills own the changelog
  voice/structure — defer to them for wording and conformance.
- **YAML (KB)** — the P2KB YAML set's own version + release notes
  (homes `TBD`).
- **INGESTION** — **not applicable.** Ingestion is version-less and has no
  release notes; it reports against quality/cross-ref/audit gates and the
  completeness dashboard instead. On the ingestion head, `build-wrapup`
  should say so rather than invent a version/notes entry.

`RELEASE_NOTES_AUDIENCE` is "the P2 developer community" for manual and
YAML release notes.
