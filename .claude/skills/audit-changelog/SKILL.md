---
name: audit-changelog
description: Audit a P2 manual's CHANGELOG.md latest entry for release readiness — verify it conforms to the manual's changelog-style-guide.md (voice/structure) AND that its claims are traceable to actual commits since the last public release. Use when the user says "audit the <manual> changelog", "is the changelog ready to release", or invokes /audit-changelog. Reports findings; does NOT auto-edit the CHANGELOG. Supports --deep flag for diff cross-reference (default is headline-level).
---

# Audit Changelog

You are auditing a P2 manual's CHANGELOG.md to verify it's ready for public release. The audit has two parts:
1. **Voice/structural conformance** — does the latest entry follow the manual's `changelog-style-guide.md`?
2. **Content correctness** — do the claims match what actually changed in commits since the last public release?

Output is a findings report grouped by severity. **You never auto-edit the CHANGELOG** — user reviews findings and decides which to act on.

## Repo layout

```
engineering/document-production/methodology/changelog-style-guide.md   # Voice/structure rules — project-wide, one canonical source
engineering/document-production/manuals/<slug>/opus-master/CHANGELOG.md # The changelog being audited
deliverables/documents/README.md                                       # Public release index — source of truth for "last released version"
```

## Step 1 — Identify the manual

If no slug given, list `engineering/document-production/manuals/*/opus-master/CHANGELOG.md` and ask which manual to audit. Accept `--deep` flag for thorough diff cross-reference.

## Step 2 — Read the inputs (in parallel)

- `engineering/document-production/methodology/changelog-style-guide.md` — the rules to apply (one canonical project-wide guide; no per-manual variants)
- `manuals/<slug>/opus-master/CHANGELOG.md` — the document being audited
- `deliverables/documents/README.md` — to learn what version is currently public

## Step 3 — Parse CHANGELOG structure

The top entry under `# <Manual Name> Changelog` is what's being audited. Parse:
- Heading: `## v<X.Y.Z> (<YYYY-MM-DD>)` — extract version + date
- Opening narrative line (`**<Type> Release** — <one-line scope>`)
- Section headings (`### <Title> (<SEVERITY>)`)
- Bullet/prose content under each section

The **second** `## v...` entry is the "last public release baseline" — its version should match `deliverables/documents/README.md`'s current entry for this manual. If they disagree, flag a discrepancy.

## Step 4 — Determine the commit baseline

In order of preference:
1. Git tag `<slug>-v<prior-version>` (e.g., `p2-pasm-desilva-style-v2.1.0`) — use if exists
2. Otherwise, find the commit that bumped `front-matter.md` (multi-file) or the cover region of the single-file master from the prior version to its successor — search via `git log -p -S "Version <prior>" -- <cover-file>`
3. As last resort, use the prior entry's date: `git log --since=<prior-date> -- manuals/<slug>/opus-master/`

Run:
```bash
git log --oneline <baseline>..HEAD -- engineering/document-production/manuals/<slug>/opus-master/
git diff --stat <baseline>..HEAD -- engineering/document-production/manuals/<slug>/opus-master/
```

If neither tag nor cover-version-bump-commit can be found, report the baseline as "approximate (date-based)" and note the audit confidence is reduced.

## Step 5 — Voice/structural audit

Apply the rules from `changelog-style-guide.md`. The guide is the authoritative source — read it fresh each run; do not hardcode rules. Common dimensions to look for in any P2 manual's guide:

- **Heading format**: matches the prescribed pattern (semver, date, parenthetical convention)
- **Opening line**: present, terse, additive framing per guide
- **Section severity tags**: vocabulary matches guide (CRITICAL / HIGH / MEDIUM / LOW or whatever the guide specifies)
- **Section ordering**: if guide prescribes an order, check it
- **Inclusion test**: any entries the guide says to EXCLUDE that crept in (process notes, root-cause explanations, internal regressions, debugging details)
- **Framing**: additive ("now provides X") vs confessional ("was wrong before") — most guides require additive
- **Aggregation**: related fixes grouped vs itemized — flag over-itemization

Additionally, apply these universal red-flag-phrase checks (independent of the per-manual guide, drawn from project-wide patterns):
- Vague capability claims: `also provides`, `eliminates`, `automatically`, `synchronizes`, `mechanism for`, `enables`, `side effect`
- Cross-version references that may break if entries are renumbered/merged: `from vX.Y.Z`, `as in vX.Y.Z`, `since vX.Y.Z` — flag for human review (legitimate uses exist)
- Marketing tone: superlatives, hype words

## Step 6 — Content audit (headline mode, default)

For each `### <Section>` in the entry:
- Extract the **headline** (section title + leading bullet/prose)
- Find supporting commits in `git log <baseline>..HEAD` whose subject line or changed-file paths plausibly match
- Flag:
  - **CHANGELOG → commits**: headline has no matching commit (overclaim or missed sourcing)
  - **commits → CHANGELOG**: significant commit (not a typo fix, not a backup file, not a `.DS_Store`) with no matching changelog mention

Use the commit-message version-tag convention (e.g., commits prefixed with `<Manual> vX.Y.Z:` or `<Manual> vX.Y.Z chunk N:`) to associate commits with the entry being audited.

## Step 7 — Content audit (deep mode, --deep flag only)

For each specific claim that names a file, chapter, section, instruction, or line number:
- Run `git diff <baseline>..HEAD -- <named-file>` (or `git log -S "<named-symbol>"`)
- Verify the claimed change is present in the diff
- For numeric claims (e.g., "8 fixes", "Ch 13/14/15"), count actual occurrences in the diff

Deep mode is slow on large refreshes (e.g., DeSilva voice refresh was 135-line diff across the canonical master). Run only when the user requests it or when headline mode surfaces material discrepancies.

## Step 8 — Report findings

Group by severity. Each finding should include:
- Line number in CHANGELOG.md
- Verbatim quote of the offending text (one sentence max)
- Specific issue (which rule from style guide, or which commit/diff disagrees)
- Suggested rewrite or action

Severity scale:
- **CRITICAL** — content factually wrong, or claims unsupported by commits (release-blocking)
- **HIGH** — voice/structural rule violations the guide marks as required; missing significant commits
- **MEDIUM** — recommended-but-not-required guide rules; minor sourcing issues
- **LOW** — stylistic suggestions, optional improvements

End the report with a one-line verdict:
- `READY` — no CRITICAL/HIGH findings
- `READY WITH NOTES` — only MEDIUM/LOW findings
- `NOT READY` — any CRITICAL or unresolved HIGH findings, list count

## What this skill does NOT do

- Does not edit CHANGELOG.md
- Does not run `prepare-manual` or `release-manual`
- Does not commit/tag/push anything
- Does not edit the style guide
- Does not validate the content of the manual itself (only the changelog)

## Error handling

- `engineering/document-production/methodology/changelog-style-guide.md` missing: stop — the canonical project-wide guide is required
- CHANGELOG.md missing or only one entry: stop — there's nothing to audit against
- Git history unavailable for baseline: report partial audit (voice only); skip content audit
- Tag not found AND cover-version-bump-commit not found: use date-based baseline with reduced-confidence note
