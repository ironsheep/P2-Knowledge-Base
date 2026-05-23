---
name: yaml-knowledge-base-maintenance
description: >-
  Edit, validate, and re-index P2 knowledge base YAMLs in place. Use
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

## 5. Regenerate the published index

```bash
python engineering/tools/generate-p2kb-index.py
```

The index is the wiring layer — consumers (agents, the p2kb-mcp server) discover content through it. Without regeneration, new or moved YAMLs are invisible to consumers even after commit + push.

If the index generator errors, fix the underlying YAML issue and retry. Never commit an index that didn't generate clean.

## 6. Re-validate after index regen

```bash
python engineering/tools/validate-crossref-keys.py
```

Both the YAMLs AND the regenerated index must be coherent. Must report clean.

## 7. Hand back

Report:
- Count of YAMLs edited
- Count of cross-references redirected per Sacred Rule #7
- Validator output (clean)
- Index regenerated (yes)
- Suggested next step: invoke `release-yamls` to publish the change

This skill does NOT commit or push — that's `release-yamls`'s job. Leave the working tree dirty for the release skill to package.

## Discipline — what NOT to do

- **Don't edit `engineering/knowledge-base/`** — transient tree; edits there have no effect on what consumers see
- **Don't delete cross-references** — Sacred Rule #7; always redirect
- **Don't use bare names in cross-references** — full paths only
- **Don't skip validation** — a YAML that validates locally but breaks the index breaks all consumers after publish
- **Don't commit a partial pass** — sweeping changes should be coherent; the release should reflect the full pass, not half of it
- **Don't run wholesale `find ... -exec edit` style batch edits** — surgical edits with a clear audit trail; the diff is the source of truth for what changed

## Error handling

- Validator reports unresolvable cross-reference → ask the user; do not delete the reference to make the error go away
- Index generator errors → stop; surface the error; fix the underlying YAML
- File you intended to edit doesn't exist → confirm with the user (might be a typo; might indicate the concept is documented elsewhere)
- `engineering/knowledge-base/` shows divergent content from `deliverables/ai/P2/` → ignore the engineering tree; flag for the cleanup skill
