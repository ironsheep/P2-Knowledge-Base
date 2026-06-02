---
name: yaml-knowledge-base-maintenance
description: >-
  Edit and validate P2 knowledge base YAMLs in place. Use
  when applying any change to deliverables/ai/P2/ — a single fix or a
  sweeping cross-data-set update from a P2KB Update Request document.
  Enforces Sacred Rule #7 (never delete cross-references; redirect to
  where content IS documented). The engineering/knowledge-base/ tree
  is transient and NOT touched by this skill.
---

# YAML knowledge base maintenance

## Canonical tree — the single source of truth

```
deliverables/ai/P2/
├── architecture/
├── language/
│   ├── fundamentals/
│   ├── pasm2/             # PASM2 instructions (~381 files)
│   └── spin2/
├── hardware/
├── community/obex/objects/
├── code-examples/
└── guides/
```

**Do not edit `engineering/knowledge-base/P2/`.** That tree is transient and stale. Its cleanup is a separate concern (see the `cleanup-backups` recommendation in the recommendations doc).

## Findability is a continually-improving asset

The KB is download-on-demand: remote agents request entries by name and follow `related:` chains to reach connected concepts. **Every time you touch a YAML, leave the remote agent better able to find what it needs than before.** This is continual, the same way process improvement is continual.

- When you observe a referencing hole — a missing cross-ref, a concept reachable under one name but not its sibling (e.g. `SETQ` documented for XBYTE but not `SETQ2`; `queue`/`queue2` not resolving), a dead-end entry — **fix it in the same pass**, not a follow-up.
- Gap/observation reports exist to *strengthen referencing and coverage*, not just patch the one reported line. Sweep the neighborhood.
- Bad findability is as harmful as bad content: a missing link means the agent silently fails to find correct info.
- This complements Sacred Rule #7 (never *remove* a cross-ref) with its active twin: proactively *add* the cross-refs and aliases a consumer would need.

## Sacred Rule #7 — Cross-references: never remove, always redirect

When a `related:` reference points at a file that doesn't exist, **find where that concept IS documented and redirect to that file**. Deleting the reference loses an intentional link.

```yaml
# WRONG — removing because end.yaml doesn't exist:
related:
  - language/spin2/assembly-directives/org.yaml
  # Removed: END

# CORRECT — END is documented in inline_pasm.yaml; redirect:
related:
  - language/spin2/assembly-directives/org.yaml
  - language/spin2/constructs/inline_pasm.yaml
```

Use **full paths** (`language/spin2/methods/exp.yaml`), not bare names (`EXP`). Full paths bypass index-generator/validator key-transformation inconsistencies.

## 1. Understand the change scope

Before editing, identify:
- What concept / instruction / topic is changing?
- Which YAML files are affected? For sweeping changes (e.g., a P2KB Update Request document), the affected set is often data-set-wide — grep first to enumerate the set so you know the work.
- What cross-references will need redirecting? Any `related:` references currently pointing at files you're about to modify, remove, or restructure?

```bash
# Enumerate affected files (example)
grep -rln "<topic-or-symbol>" deliverables/ai/P2/

# Enumerate inbound cross-references to a file you're about to change
grep -rln "<path/to/target.yaml>" deliverables/ai/P2/
```

## 2. Edit in place

For each affected YAML:
- Use `mcp__filesystem__edit_file` or `Edit` for surgical changes. Never wholesale-replace.
- For files >100 lines or >50KB, create a timestamped backup first per Sacred Rule #1 (`<file>.backup.YYYYMMDD_HHMMSS`). Backups are git-ignored; `cleanup-backups` clears them at release time.
- Preserve unrelated structure, formatting, and ordering. Diffs should show only the intentional changes.
- For sweeping changes, work in passes: identify the pattern, apply consistently across the affected set, then move to the next pattern. Don't mix concerns within a single editing pass — it makes the diff harder to review.

## 2.5 Verify YAML format

**MANDATORY before any downstream script.** A YAML parse error introduced during editing is far cheaper to catch here than to discover after the index generator silently skips the broken file (or after a consumer LLM downloads it and chokes on the parse).

```bash
# Targeted check on the files you just edited:
python engineering/tools/verify-yaml-format.py --files <edited_file_1> <edited_file_2> ...

# Tree-wide baseline (slower but exhaustive; useful pre-release):
python engineering/tools/verify-yaml-format.py
```

The verifier reports per-file parser errors with paths + messages. Fix every reported error before proceeding to step 3.

Common parse failures introduced during editing:

- Unquoted strings containing special characters — e.g., `- "Prop" checksum mechanism` mixes a quoted scalar with unquoted text and is invalid. Quote the whole thing: `- 'Prop checksum mechanism'`
- A line that starts with `"X"` followed by more text is parsed as `"X"` plus garbage
- Tabs vs. spaces mixed in indentation
- Misaligned block structure after copy-paste
- Trailing `:` on a line where a value is expected

Do **not** proceed to step 3 with parse errors.

## 3. Sweep for cross-reference impact

Any file you removed, renamed, or significantly restructured may break inbound `related:` references. After edits, sweep:

```bash
grep -rln "<path/to/edited.yaml>" deliverables/ai/P2/
```

For each match, decide: does the reference still point at correct content? If the referenced content moved or changed shape, **redirect** the reference per Sacred Rule #7. Never just delete.

## 4. Validate cross-references

```bash
python engineering/tools/validate-crossref-keys.py
```

Fix any reported issues — usually broken `related:` references that need redirecting. Re-run until clean. Do **not** proceed to step 5 with validator errors.

**Note on the published index during validation:** The cross-ref validator reads the published `deliverables/ai/p2kb-index.json` to know what keys exist. If you've created new YAML files in this session, the published index won't know about them yet and the validator will report false unresolved references. To validate, run a **throwaway** index regeneration (`python engineering/tools/generate-p2kb-index.py`) so the validator can see the new keys — but **do NOT stage or commit this index**. The index generator records each file's git commit timestamp via `git log -1 --format=%ct`, so a working-tree regen produces filesystem-mtime placeholders for files that haven't been committed yet. The correct, ship-able index is produced by `release-yamls` AFTER the content commit, with all files having proper commit timestamps.

If you regenerated the index for validation, leave it in the working tree but unstaged. `release-yamls` will overwrite it with the post-commit regen.

## 5. Hand back

Report:
- Count of YAMLs edited
- Count of cross-references redirected per Sacred Rule #7
- Validator output (clean)
- Suggested next step: invoke `release-yamls` to publish the change

The published index is NOT regenerated in this skill. That happens in `release-yamls` AFTER the content is committed, so the index records correct git commit timestamps.

This skill does NOT commit or push — that's `release-yamls`'s job. Leave the working tree dirty for the release skill to package.

## Content discipline for download-on-demand context cost

The P2KB is a **download-on-demand system**. Every YAML loaded into a consumer LLM's context costs tokens — and a single user question often pulls a chain of 3-8 files via `related:` cross-references. A 250-line entry is 30% of a typical small-model context window just from one file.

**Brevity is a feature, not a flaw.** When in doubt, cut.

### Line-budget rules of thumb

| Entry type | Target | Hard ceiling |
|------------|--------|--------------|
| Index files (`_index.yaml`) | ≤100 lines | 150 |
| Instruction entries (single PASM2 op) | ≤80 lines | 120 (only if instruction is genuinely complex — e.g., XINIT, COGINIT) |
| Architecture entries (single concept) | ≤150 lines | 200 |
| Code-example / case-study entries | ≤150 lines | 200 |
| Idiom files | ≤100 lines | 150 |
| Concept entries (multi-instruction topics) | ≤250 lines | 400 (only for true subsystem-level coverage) |

Files exceeding the hard ceiling should split into sub-entries — the index file then names the sub-entries, and consumers pull only the sub-entry they need.

### Content-shape principles

- **Cross-link, don't duplicate.** If concept X is documented in `file_a.yaml`, file_b.yaml should reference it, not restate it. The reader follows the link only if they need the depth.
- **One `related:` block per file** with full paths. Don't maintain parallel `related:` + `canonical_entries:` + `see_also:` blocks unless they have meaningfully different roles. Duplicated cross-refs bloat every file that touches a topic.
- **Diagnostic / troubleshooting / "how to configure" prose belongs in separate files**, not embedded in concept entries. A consumer asking "what is X?" should not pay context for "here's how to troubleshoot X."
- **Resist comprehensive cross-referencing.** Include the cross-refs a consumer is likely to actually follow from this file. Don't preemptively list every distantly-related file.
- **Failure modes / caveats / edge cases get terse one-liners**, not paragraphs. A consumer who needs depth on a specific failure mode will pull the specific file that documents it.
- **Confidence-tier metadata is load-bearing only when content is genuinely uncertain.** For verified facts from primary sources, no tier markers needed. For preliminary research, prefer to OMIT the unverified content rather than ship it with caveats (downstream LLMs may strip the caveats and propagate the content as authoritative).

### When you're tempted to add detail

Ask: **"Will the typical consumer of this file actually use this content, or am I writing it because I have it?"**

If the consumer would more naturally pull a different file for that detail, link to that file instead. The brevity comes from the system, not from any one file being exhaustive.

### Self-check before completing edits

After your edits, eyeball each touched file:
- Is it within the line target for its type?
- Are there blocks that duplicate content cross-linked elsewhere?
- Are there blocks of guidance / diagnostics / examples that could be their own file?
- Are there `related:` entries that are reflexive (file_a → file_b → file_a) without adding value?

If yes to any: trim before moving on.

## Discipline — what NOT to do

- **Don't edit `engineering/knowledge-base/`** — transient tree; edits there have no effect on what consumers see
- **Don't delete cross-references** — Sacred Rule #7; always redirect
- **Don't use bare names in cross-references** — full paths only
- **Don't skip YAML format verify (Step 2.5)** — broken YAML caught after index regen is much more expensive to fix
- **Don't skip cross-ref validation** — a YAML that validates locally but breaks the index breaks all consumers after publish
- **Don't commit a partial pass** — sweeping changes should be coherent; the release should reflect the full pass, not half of it
- **Don't run wholesale `find ... -exec edit` style batch edits** — surgical edits with a clear audit trail; the diff is the source of truth for what changed
- **Don't over-inflate entries** — line budgets exist for a reason; long files cost downstream context tokens on every consumer download
- **Don't ship unverified preliminary content with caveats** — downstream LLMs may strip the caveats and propagate as authoritative; prefer to OMIT the unverified content and document the gap with a chase pointer

## Error handling

- Validator reports unresolvable cross-reference → ask the user; do not delete the reference to make the error go away
- Index generator errors → stop; surface the error; fix the underlying YAML
- File you intended to edit doesn't exist → confirm with the user (might be a typo; might indicate the concept is documented elsewhere)
- `engineering/knowledge-base/` shows divergent content from `deliverables/ai/P2/` → ignore the engineering tree; flag for the cleanup skill
