# P2-Knowledge-Base overlay — document-finalize

This project finalizes **technical** documents (P2 manuals, the P2KB YAML
set) whose claims are consumed downstream — by readers and by remote AI
agents generating code. `DELIVERABLE_AUDIENCE` splits them: manuals are
`human-reader`, the YAML set is `agent-consumer`, so central §5's strict bar
(**cite the authority or omit the entry**) is the live one whenever the finalize
pass touches the KB. These augments tighten the audit and the handback
accordingly. Manuals render on **PDF Forge** (handback model —
`DOC_RENDER_COMMAND` is unset by design), so the §5/§6 handback *is* the
deliverable, and it must be located precisely enough for {{USER_NAME}} to
verify against the rendered PDF in one pass.

## Augments §1 — Audit and gather every finding

Central §1 now owns claim verification itself: judge every domain assertion
against `{{DOMAIN_AUTHORITY}}` and classify it. This overlay adds only what is
project-shaped on top of that.

- **The truth matrix comes first.** Before judging any claim, build the matrix
  from the sources the slot names — the framework is
  `engineering/operations/process/TECHNICAL-DOCUMENT-AUDIT-METHODOLOGY.md`, and
  each manual's `creation-guide.md` names its own verification sources on top of
  the project-wide precedence.
- **This project's classification is four-valued**, and the extra value carries
  information central's three do not. Map it as: `VERIFIED` → verified;
  `UNVERIFIED` → unverified; `MODIFIED` and `FABRICATED` are both *contradicted*,
  but they are logged distinctly — MODIFIED means the source says something
  different, FABRICATED means the source says nothing at all and the claim was
  invented. Do not collapse them; the fabrication rate is what the audit
  methodology tracks.
- **Watch the red-flag phrases** that tend to precede fabrication: "also
  provides", "side effect", "eliminates", "automatically",
  "synchronizes", "mechanism for", vague "enables …". Treat each as a
  prompt to go re-verify against a source.
- **Watch the *shape* as well as the vocabulary — the payoff sentence.**
  *(Locally adopted 2026-07-20, promotion-pending — see the
  `sprint-retrospective` overlay's adopt → certify → promote model.)*
  The red-flag list above catches a **word choice**. The costlier failure
  in narrative-voice documents is a **sentence structure**: a closing
  crescendo ("that is a remarkable amount of insight for two
  instructions…") creates a slot that demands a punchy technical payoff,
  and when no true one is available an invented one fills it. At write
  time, whenever you close a section or a `:::` callout with a flourish,
  **strip the rhetoric and read what is left as a bare claim** — then
  satisfy it or delete it. Two cheap tests, neither needing a source:
  *(a)* does the document already say the opposite somewhere else?
  *(b)* does the sentence lean on `never · always · every · only ·
  everyone · nothing · impossible · forever · free · the single most`?
  Beware **hedge-drop** — stating a fact correctly with its small print,
  then restating it absolutely a few sections later. A number advertising
  its own rigour ("not a claim from theory — it is measurable") must name
  its source in the same breath. Detection-side counterpart:
  `document-audit` Dimension #4c. (Origin: the XBYTE guide, where an
  external expert found one such claim and the sweep found four more, all
  refutable from the document itself.)
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

## Augments §1 — app-note elements carry a doc↔companion agreement check

When the `active_element` is an **app note** (a document-production element
alongside manuals — see `HEAD-DISPATCH-DRAFT.md` §"Artifact-type model"), the
finalize batch includes one extra finding source: the **doc↔YAML-companion
agreement**. An app note ships as the human doc **+ a first-party YAML companion**
under `deliverables/ai/P2/` (a digest+links, never a prose clone). Before
sign-off, confirm the companion's composition recipe, parameters/pin-maps, and
code reference still match the finalized doc — a divergence is a release-blocking
finding, gathered in this pass like any other. The gate itself is owned by
`document-audit`; the companion is governed by `yaml-knowledge-base-maintenance`;
the principle is in
`engineering/document-production/app-notes/APP-NOTE-DESIGN-DECISIONS.md`.

## Augments the fix step — example edits keep loose-file ↔ code-block identity

When a manual ships an **example corpus** (a `manuals/<slug>/examples-library/`
of loose `*.spin2` files, bundled as `examples-library.zip` for the reader), the
loose file a reader opens in an external tool **must be byte-identical to the
printed code block** in `opus-master/` that carries `caption="<name>.spin2"`
([[feedback_example_file_matches_code_block_not_figure]]). Identity — not the
rendered figure matching the published screenshot, and not compile/run success
(those are `pnut-ts -d` and the hardware run-list, separate gates).

- **Edit both halves in lockstep.** When a finding touches an example, change the
  loose `examples-library/<name>.spin2` **and** its `opus-master` code block in the
  same pass. Never one without the other.
- **Gate before the re-zip.** Before rebuilding `examples-library.zip` (and before
  calling the corpus done for this cycle), run the identity checker — it must be
  **GREEN**:

  ```bash
  python3 engineering/tools/verify-example-corpus-identity.py            # default: Debug Window
  python3 engineering/tools/verify-example-corpus-identity.py --manual <manual-dir>   # any other
  ```

  A RED result (mismatch / orphan loose-file / orphan block / duplicate caption)
  is a corpus-drift defect — resolve it, do not re-zip over it. Exit 0 = GREEN.

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
