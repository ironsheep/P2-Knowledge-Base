# P2-Knowledge-Base overlay — release-manual

This project ships **technical** manuals whose claims are consumed by readers
and by remote AI agents. Some manuals also ship a **reader example corpus** — a
`manuals/<slug>/examples-library/` of loose `*.spin2` files bundled as
`examples-library.zip` and published next to the PDF. A loose file that has
silently drifted from the manual's printed code block is a trust defect the
reader hits in their editor, so the release must guard against it exactly as
Phase 1 guards against silent PDF content-drop.

## Augments Phase 1 — VERIFY: add the example-corpus identity gate

For any manual that publishes an `examples-library.zip`, the PDF silent-drop
check is **not sufficient** — also verify the example corpus has not drifted:

- **Run the identity checker; it must be GREEN before the ZIP is published**
  (before the `git add -f …-src.zip` in Phase 5, and before any re-zip):

  ```bash
  python3 engineering/tools/verify-example-corpus-identity.py            # default: Debug Window
  python3 engineering/tools/verify-example-corpus-identity.py --manual <manual-dir>   # any other
  ```

  Exit 0 = GREEN (every loose `*.spin2` is byte-identical to its `opus-master`
  code block, no orphan files/blocks, no duplicate captions). A RED result
  **blocks the release** — the published ZIP would hand readers files that don't
  match the printed manual ([[feedback_example_file_matches_code_block_not_figure]]).

- **Re-zip only from a GREEN corpus.** If you rebuild `examples-library.zip`
  during the release, run the checker first; never zip over a drifted corpus.

- Manuals with **no** `examples-library/` (reference-only manuals) skip this gate
  — the checker prints GREEN and exits 0 when no corpus is present, so it is safe
  to run unconditionally.

## Augments Phase 1 — VERIFY: the in-doc Revision History agreement gate

Every **app note** (and any document that prints a `## Revision History` in its body —
**no manual currently does; grep, don't assume**) states its version in a place the
reader actually reads, *separate* from the cover and from `CHANGELOG.md`. Phase 2a audits
`CHANGELOG.md`; **nothing looked at the rendered Revision History**, so the two drifted
silently — and the *release itself* was the thing causing the drift, because it bumped the
cover and left the table behind (F-215: four app notes shipped a cover version that appears
nowhere in their own history).

**Authoring this belongs to `prepare-manual` (see its `project-overlay.md`), not here** —
the Revision History is inside the body markdown that gets rendered, and by the time this
skill runs the PDF already exists. This gate is the **backstop**: it catches a miss, and a
miss costs a full re-render.

**Assert against the RENDERED PDF (not the source — the source may be right and the PDF
stale from an earlier build):**

```bash
PDF=deliverables/documents/DOCs/<PDF>
COVER=$(pdftotext -f 1 -l 1 "$PDF" - | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" | head -1)
TOP=$(pdftotext "$PDF" - | grep -A4 -i "^Revision History" | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" | head -1)
echo "cover=$COVER  revision-history-top=$TOP"
```

Both must hold:
1. **`TOP` == `COVER`** — the document's own history lists the version it *is*.
2. **No never-shipped version is named anywhere in the section.** Authority is `git tag`,
   not the CHANGELOG: `git tag | grep -i "<slug>"`. Any `0.x` review draft is *not* a
   release and must not appear.

**A mismatch BLOCKS the release** exactly as a content-drop does: fix the Revision History
in `opus-master`, re-prepare, regenerate, re-verify. Do not promote a document whose own
history contradicts its cover.

> **Detection note (why F-215 was under-counted on first pass):** the original sweep grepped
> for the literal `v0.1.0` / "initial draft" and so missed four app notes whose tables say a
> bare `0.1.0` / "First draft". **Key on the shape of the defect (a version < the cover, or a
> version with no tag), never on one spelling of it.**
