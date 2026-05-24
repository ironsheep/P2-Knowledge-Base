<!-- Requires MCP: p2kb-mcp (only for the local-cache refresh step; everything else is git+filesystem) -->
---
name: release-yamls
description: >-
  Release the P2 knowledge base YAMLs — pick a new repo version per the
  user's bump-granularity call, update CHANGELOG.md and the README
  version badge, drive the two-commit publish flow (content commit, then
  index commit against the committed-content state), and refresh the
  local p2kb-mcp cache after push. Use after yaml-knowledge-base-
  maintenance has produced a clean, validated working tree. The
  published index is regenerated INSIDE this skill, after the content
  commit, so file mtimes record real git commit timestamps.
---

# Release YAMLs

## Source of truth for the repo's KB version

The **latest git tag** is canonical. The README badge and CHANGELOG top entry should both mirror it. This skill aligns them on each release.

```bash
git tag --list | grep -E '^v[0-9]' | sort -V | tail -1
```

If the badge or CHANGELOG drift behind the latest tag, that's a pre-existing inconsistency — this skill is the moment to correct it as part of the new release.

## Why this is a two-commit release

The published index (`deliverables/ai/p2kb-index.json`) is **derived** from the content YAMLs. Its `mtime` field for each entry is the file's **git commit timestamp** (`git log -1 --format=%ct`), with filesystem mtime as fallback for never-committed files. That means:

- Regenerating the index BEFORE the content is committed produces incorrect mtimes: new files get filesystem mtimes (placeholder), modified files get OLD commit timestamps (pre-edit). Shipping that index gives consumers misleading change-detection signals.
- Regenerating the index AFTER the content is committed produces CORRECT mtimes — every file's `mtime` reflects the actual commit it shipped in.

This skill enforces the correct order:

1. Stage and commit content (YAMLs, docs, skills, tools) — **no index files**
2. Regenerate index against the just-committed state
3. Validate the fresh index
4. Stage and commit the index
5. Tag the index commit (the one consumers fetch)
6. Push both commits + tag

## 1. Verify precondition — YAML work is ready to publish

Before bumping anything, confirm the working tree reflects a clean YAML-maintenance pass:
- `deliverables/ai/P2/` edits are made and ready
- YAML format clean: `python engineering/tools/verify-yaml-format.py`
- Cross-references clean: `python engineering/tools/validate-crossref-keys.py`
- No `*.backup.*` files staged (they're git-ignored, but verify with `git status`)

Note: `yaml-knowledge-base-maintenance` may have left a working-tree-state index file (`deliverables/ai/p2kb-index.json` showing as modified) from a throwaway regen used for validation. That's fine — DO NOT stage it. This skill will overwrite it with a post-commit regen in Step 6b.

If the validators haven't been run, stop and tell the user to complete `yaml-knowledge-base-maintenance` first. Do not release an unvalidated KB.

## 2. Determine the new version

Read the current version (latest semver tag). Ask the user directly in chat for the bump tier:

- **Patch** — bug fix or small correction; increment patch only (e.g., `1.4.3` → `1.4.4`)
- **Minor** — additive changes (new instructions, expanded patterns, new documentation, non-breaking updates); zero patch (e.g., `1.4.3` → `1.5.0`)
- **Major** — breaking changes (schema change, removed content, restructured KB); zero minor and patch (e.g., `1.4.3` → `2.0.0`)

**The patch-zero rule is enforced by the skill, not the user.** The user picks the tier; you compute the resulting version. Never propose `1.5.3` from a `1.4.3 → minor` decision. Major bumps zero both minor and patch.

If no tags matching `^v[0-9]` exist, stop and ask the user for the bootstrap version (e.g., `v1.0.0`).

## 3. Update the README version badge

The badge in top-level `README.md` is a hardcoded shields.io URL:

```markdown
[![Version](https://img.shields.io/badge/version-X.Y.Z-blue.svg)](https://github.com/ironsheep/P2-Knowledge-Base/releases)
```

Edit the `version-X.Y.Z` segment to the new version. The badge is the most visible version artifact for repo readers; keeping it aligned with the tag is the reason this skill exists.

## 4. Add a CHANGELOG entry

Add a new entry at the top of `CHANGELOG.md` — **below the "Manual Releases" index table, above the previous semver entry**. The Manual Releases table is for PDF manuals and shouldn't be disturbed.

Format follows Keep a Changelog (the file's existing convention):

```markdown
## [X.Y.Z] - YYYY-MM-DD

**[One-line release theme]**

### [Added | Changed | Fixed | Removed]
- Bullet describing change in user-facing terms
- ...
```

Voice **must** follow `engineering/document-production/methodology/changelog-style-guide.md`. Re-read the style guide every release — its discipline (optimistic forward-looking voice, never describe prior wrong state, never-shipped versions never mentioned, internal housekeeping stays silent) is load-bearing. Run each bullet through the two-question gate at the end of the style guide before keeping it.

If a stale `## [X.Y.Z] - YYYY-MM-DD (Upcoming)` entry exists at the top (older planning artifact that never shipped), **delete it** — never-shipped versions are never mentioned.

Ask the user directly in chat for the release theme and key bullets if not obvious from the working-tree diff (`git diff --stat`).

## 5. Show plan, confirm

Ask the user directly in chat (do NOT use the AskUserQuestion tool in this repo — see project memory). Show:
- Current version → new version
- README badge before/after (one line each)
- New CHANGELOG entry preview
- Count of content files about to be staged (`git status --short | grep -v "<pre-existing untracked to skip>" | wc -l`)
- Reminder: index is NOT staged at content commit; gets regenerated and committed separately

Offer: proceed / cancel.

## 6. Execute the two-commit release

Per CLAUDE.md, git actions need explicit user authorization. The default is to **suggest** the commands and have the user run them. If the user explicitly authorizes execution ("commit and push", "do it", etc.), execute the steps below. Otherwise, print them as a script for the user to copy-run.

### 6a. Commit content (without the index)

Stage all content changes EXPLICITLY — never use `git add .` or `git add -A`. The explicit list ensures pre-existing untracked files that aren't part of this release stay out:

```bash
git add \
  <list each modified/new file or directory explicitly> \
  README.md \
  CHANGELOG.md
# DO NOT add: deliverables/ai/p2kb-index.json or .gz at this step
```

Verify staging with `git status --short`. Confirm the index files are NOT staged.

```bash
git commit -m "$(cat <<'EOF'
Release P2 Knowledge Base v<X.Y.Z>: <one-line theme>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

The Co-Authored-By line is optional; include only if the user wants the agent attributed.

### 6b. Regenerate the published index against the committed state

```bash
python engineering/tools/generate-p2kb-index.py
gzip -c deliverables/ai/p2kb-index.json > deliverables/ai/p2kb-index.json.gz
```

Now every entry's `mtime` field is the file's actual v<X.Y.Z> commit timestamp.

### 6c. Validate the fresh index

```bash
python engineering/tools/validate-crossref-keys.py    # expect 100% resolution
python engineering/tools/validate-dod-release.py      # expect ALL VALIDATIONS PASSED
```

Both must pass. If validation fails, fix the underlying issue and re-regen the index. Do NOT proceed to the index commit with validation errors.

### 6d. Commit the index

```bash
git add deliverables/ai/p2kb-index.json deliverables/ai/p2kb-index.json.gz
git commit -m "Regenerate published index for v<X.Y.Z>"
```

### 6e. Tag (the INDEX commit) and push

The tag must point at the index commit — that's the state consumers will fetch.

```bash
git tag -a v<X.Y.Z> -m "P2 Knowledge Base v<X.Y.Z>"
git push origin main
git push origin v<X.Y.Z>
```

## 7. After push — refresh the local p2kb-mcp cache

The p2kb-mcp server in this container caches the published index. After the user confirms the push succeeded (or after you've executed the push), refresh the cache so this agent (and any other local consumer) sees the published state instead of stale cached content:

```
mcp__p2kb-mcp__p2kb_refresh
```

Invoke it; report the returned status.

This step is relevant **only when p2kb-mcp is installed locally** (this container has it; some deployments don't). For agents consuming the published GitHub state via web fetch or remote MCP, push alone is sufficient — they pick up the new state without a refresh call.

If the push hasn't happened yet, do not refresh — the cache would just re-load the pre-push state. Wait for confirmation.

## Hand back

Report:
- New version: `vX.Y.Z`
- Content commit hash + index commit hash
- README badge updated, CHANGELOG entry added (style-guide compliant)
- Tag created, pushed
- Local p2kb-mcp refresh status

## What this skill does NOT do

- Does not edit YAMLs (`yaml-knowledge-base-maintenance` does that)
- Does not auto-execute git commands without explicit user authorization (per CLAUDE.md)
- Does not handle PDF manual releases (`release-manual` does)
- Does not handle AI-package releases (separate candidate, not built)
- Does not auto-refresh remote consumers — only the local MCP cache after push
- Does not use the `AskUserQuestion` tool (this repo's convention is direct chat questions)

## Error handling

- No git tags matching `^v[0-9]` → stop, ask user for bootstrap version
- README badge URL doesn't match the expected `version-X.Y.Z` pattern → stop, ask user how to handle
- CHANGELOG `## [X.Y.Z]` heading convention doesn't match → stop, ask
- Validator hasn't been run against the working tree → recommend completing `yaml-knowledge-base-maintenance` first; do not proceed
- Index file shown as modified before Step 6 → this is the throwaway-regen artifact from yaml-knowledge-base-maintenance; DO NOT stage it for the content commit; Step 6b will overwrite it
- Step 6c validation fails after the fresh index regen → STOP; the content commit is already in history. Fix the issue (likely a missed cross-reference), regen index, retry validation. Do NOT push until clean.
- Push fails (network, auth, hook) → the user handles; do not retry from the skill
- `p2kb_refresh` fails after push → report the error to user; the published state is still correct, only the local cache is stale
