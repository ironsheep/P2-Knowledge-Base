<!-- Requires MCP: p2kb-mcp (only for the local-cache refresh step; everything else is git+filesystem) -->
---
name: release-yamls
description: >-
  Release the P2 knowledge base YAMLs — pick a new repo version per the
  user's bump-granularity call, update CHANGELOG.md and the README
  version badge, suggest commit + tag + push commands, and refresh the
  local p2kb-mcp cache after push. Use after yaml-knowledge-base-
  maintenance has produced a clean, validated working tree with a
  regenerated index. Publishing = commit + push; until pushed, no
  consumer sees the change.
---

# Release YAMLs

## Source of truth for the repo's KB version

The **latest git tag** is canonical. The README badge and CHANGELOG top entry should both mirror it. This skill aligns them on each release.

```bash
git tag --list | grep -E '^v[0-9]' | sort -V | tail -1
```

If the badge or CHANGELOG drift behind the latest tag, that's a pre-existing inconsistency — this skill is the moment to correct it as part of the new release.

## 1. Verify precondition — YAML work is ready to publish

Before bumping anything, confirm the working tree reflects a clean YAML-maintenance pass:
- `deliverables/ai/P2/` edits are made and ready
- Validator clean: `python engineering/tools/validate-crossref-keys.py`
- Index regenerated: `python engineering/tools/generate-p2kb-index.py`
- No `*.backup.*` files in the staged set (they're git-ignored, but verify with `git status`)

If validator or index hasn't been run with the latest edits, stop and tell the user to complete `yaml-knowledge-base-maintenance` first. Do not release an unvalidated KB.

## 2. Determine the new version

Read the current version (latest semver tag). Ask the user with `AskUserQuestion` for the bump tier:

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

Edit the `version-X.Y.Z` segment to the new version using `mcp__filesystem__edit_file`. The badge is the most visible version artifact for repo readers; keeping it aligned with the tag is the reason this skill exists.

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

Voice follows `engineering/document-production/methodology/changelog-style-guide.md`: terse, additive, user-focused, no internal-process notes, no file paths, no commit SHAs, no audit IDs.

If a stale `## [X.Y.Z] - YYYY-MM-DD (Upcoming)` entry exists at the top (older planning artifact that never shipped), **replace it** with the actual release entry rather than adding above. Stale "Upcoming" entries are noise.

Ask the user for the release theme and key bullets if not obvious from the working-tree diff (`git diff --stat`).

## 5. Show plan, confirm

Use `AskUserQuestion` to show:
- Current version → new version
- README badge before/after (one line each)
- New CHANGELOG entry preview
- Count of YAMLs and other files about to be staged (`git status --short | wc -l`)

Offer: proceed / cancel.

## 6. Suggest commit + tag + push (do NOT execute)

Per CLAUDE.md, git actions need explicit user authorization. Suggest the commands; do not run them:

```bash
# Stage the release
git add \
  deliverables/ai/P2/ \
  deliverables/ai-reference/ \
  README.md \
  CHANGELOG.md

git commit -m "Release P2 Knowledge Base v<X.Y.Z>: <one-line theme>"

# Tag and push
git tag -a v<X.Y.Z> -m "P2 Knowledge Base v<X.Y.Z>"
git push origin main
git push origin v<X.Y.Z>
```

Verify the staged paths include the regenerated index file(s) — the exact path depends on what `generate-p2kb-index.py` wrote (usually under `deliverables/ai-reference/`). Check with `git status` before suggesting; adjust the `git add` list to match.

**Tell the user**: "Run those when ready. Publishing = commit + push; until pushed, no consumer sees the change."

## 7. After push — refresh the local p2kb-mcp cache

The p2kb-mcp server in this container caches the published index. After the user confirms the push succeeded, refresh the cache so this agent (and any other local consumer) sees the published state instead of stale cached content:

```
mcp__p2kb-mcp__p2kb_refresh
```

Invoke it; report the returned status.

This step is relevant **only when p2kb-mcp is installed locally** (this container has it; some deployments don't). For agents consuming the published GitHub state via web fetch or remote MCP, push alone is sufficient — they pick up the new state without a refresh call.

If the user reports the push hasn't happened yet, do not refresh — the cache would just re-load the pre-push state. Wait for confirmation.

## Hand back

Report:
- New version: `vX.Y.Z`
- README badge updated, CHANGELOG entry added
- Git commands suggested (await user's execution)
- After push: local p2kb-mcp refresh status

## What this skill does NOT do

- Does not edit YAMLs (`yaml-knowledge-base-maintenance` does that)
- Does not run git commands (per CLAUDE.md — user authorizes)
- Does not push to remote
- Does not handle PDF manual releases (`release-manual` does)
- Does not handle AI-package releases (`release-ai-package` is a separate candidate in the recommendations doc, not built)
- Does not auto-refresh remote consumers — only the local MCP cache after push

## Error handling

- No git tags matching `^v[0-9]` → stop, ask user for bootstrap version
- README badge URL doesn't match the expected `version-X.Y.Z` pattern → stop, ask user how to handle
- CHANGELOG `## [X.Y.Z]` heading convention doesn't match → stop, ask
- Validator hasn't been run against the working tree → recommend completing `yaml-knowledge-base-maintenance` first; do not proceed
- Push fails (network, auth, hook) → the user handles; do not retry from the skill
- `p2kb_refresh` fails after push → report the error to user; the published state is still correct, only the local cache is stale
