# P2-Knowledge-Base overlay — document-finalize

This project finalizes **technical** documents (P2 manuals, the P2KB YAML
set) whose claims are consumed downstream — by readers and by remote AI
agents generating code. A wrong claim is not cosmetic; it corrupts what
the consumer produces. These augments tighten the audit and the handback
accordingly. Manuals render on **PDF Forge** (handback model —
`DOC_RENDER_COMMAND` is unset by design), so the §5/§6 handback *is* the
deliverable, and it must be located precisely enough for {{USER_NAME}} to
verify against the rendered PDF in one pass.

## Augments §1 — Audit and gather every finding

The central step gathers findings. For technical documents, **how** a
finding is judged correct is not freeform — it follows the project's
audit doctrine:

- **Verify against primary sources, not memory.** Build a truth matrix
  from the golden sources before judging a claim. Authority order for P2
  language facts: `pnut_ts` compiler → Spin2 v55 docs
  (`engineering/ingestion/sources/spin2-v55/`) → Silicon Doc. The full
  framework is `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`;
  each manual's `creation-guide.md` names its own verification sources.
- **Classify every extracted claim** as `VERIFIED` / `MODIFIED` /
  `UNVERIFIED` / `FABRICATED` — do not leave a claim unclassified.
- **Watch the red-flag phrases** that tend to precede fabrication: "also
  provides", "side effect", "eliminates", "automatically",
  "synchronizes", "mechanism for", vague "enables …". Treat each as a
  prompt to go re-verify against a source.
- **`NEEDS-VERIFICATION` is not a license to ship.** A finding labelled
  needs-verification is *not* permitted to carry past this finalize pass
  if the sources to resolve it are in the repo. Before closing the
  inventory, sweep for `NEEDS-VERIFICATION` items and resolve each one
  whose golden source is available *in this pass*. Only items needing
  something genuinely absent (hardware measurement, a source not in the
  repo) may carry forward — and say so explicitly. (See
  [[feedback_needs_verification_not_a_ship_license]],
  [[feedback_no_deferring_work]].)
- **Correctness findings that touch the P2KB YAML set go in the
  consolidated register**, `engineering/operations/P2KB-CORRECTION-FINDINGS.md`,
  not only in this document's inventory — that register is the handoff to
  the `yaml-knowledge-base-maintenance` agent. (See
  [[project_p2kb_corrections_register]].) A manual-only finding stays in
  the document's own inventory / `audit/` folder.
- **Pull in the manual's punch-list.** Updating a manual is the moment to
  clear its deferred nits, not just the change that triggered the pass — a
  render is happening anyway, so queued fixes should ride along. Read the
  manual's `workspace/<slug>/PUNCH-LIST.md` (and scan the cross-manual
  `engineering/document-production/PUNCH-LIST.md` for items scoped to this
  manual). Fold every **OPEN** item that fits the current batch into this
  pass's inventory; an item genuinely out of scope stays on the list with a
  one-line why. This is the batching discipline
  ([[feedback_batch_and_verify_workflow]]) applied to the standing backlog,
  not just this cycle's findings.

## Augments the fix step — apply each fix in the correct tree

P2 manuals are **multi-tree**: edit the wrong one and the fix is silently lost
on the next assemble. Before applying any finding, decide where it lands.

- **Content fixes → `manuals/<slug>/opus-master/`.** ALL document prose and
  structure is authored here — chapter/appendix text, part intros, and the
  cover/front-matter (`front-matter.md`, *including* its `{=latex}` cover-layout
  block). This is the canonical source. A cover that overflows, a jumbled
  appendix, missing part intros, an index tag, a clickable cross-reference — all
  opus-master edits.
- **NEVER edit `workspace/<slug>/<DocName>.md`.** That assembled working copy is
  a build artifact — `prepare-manual` regenerates it from opus-master on every
  run (`assemble-manual.sh` for multi-file, a copy for single-file), so any edit
  there is overwritten and lost. If you catch yourself editing the workspace
  `.md`, stop: the fix belongs in opus-master.
- **Style fixes → `workspace/<slug>/templates/` & `filters/`, or `platform/`.**
  The stylesheets (`*.latex`, `*.sty`) and Lua filters (`*.lua`) define
  *presentation*; edit them in place. Shared platform files (`p2kb-platform-*`)
  live under `engineering/document-production/platform/` and are edited there,
  never copied into a manual. `assemble-manual.sh` (chapter order) is a workspace
  build script, edited in workspace.
- **The discriminator:** editing the **document** (what it says / its
  front-matter) → opus-master; editing the **stylesheet/template/filter** (how it
  looks) → workspace or platform. When a single finding spans both — e.g. an
  index needs `\index{}` tags (content → opus-master) *and* `\makeindex`/`\printindex`
  (template → workspace) — split it and edit each part in its own tree.

## Augments §5–§6 — Render once, then verify / Hand back

Because manuals render on PDF Forge (not a local `DOC_RENDER_COMMAND`),
the handback is the verify-list {{USER_NAME}} works from — and PDF
generation is the *expensive* step, so batch to minimize passes:

- **Locate every verify item.** Each item in the handback verify-list
  states **which chapter** and the **within-chapter section/subsection**
  (e.g. "Ch 11 §11.2, under '### Frame Format'"), plus figure/table
  number when known — never a bare figure name. Grep the master for the
  heading just above the item if unsure. (See
  [[feedback_diagram_review_locations]].)
- **Batch the pass; don't trickle single fixes.** Fix everything in scope
  this cycle, stage one bundle, then present the full located verify-list.
  A fix-one-then-regenerate loop wastes the expensive render. Confidence
  permitting, finish a whole category rather than a token batch. (See
  [[feedback_batch_and_verify_workflow]].)
- **Keep a running cross-cycle list.** Items {{USER_NAME}} confirms drop
  off; new items the render surfaces get added to the next cycle's
  inventory. todo-mcp is the home for the in-flight list.
