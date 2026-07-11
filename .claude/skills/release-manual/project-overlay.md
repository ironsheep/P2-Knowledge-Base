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
  (before the `git add -f …-src-YYMMDD.zip` in Phase 5, and before any re-zip):

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
