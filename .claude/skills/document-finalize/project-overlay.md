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
  language facts: `pnut_ts` compiler → Spin2 v51 docs
  (`engineering/ingestion/sources/spin2-v51/`) → Silicon Doc. The full
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
