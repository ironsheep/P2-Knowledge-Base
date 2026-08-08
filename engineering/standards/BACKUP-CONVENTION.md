# Backup convention

**Established:** 2026-08-08
**Applies to:** the entire workspace — every tree, tracked or not.
**Enforced by:** `engineering/tools/backup-file.sh` + one `.gitignore` rule (`/.backups/`)

---

## The rule

Every safety copy required by **Sacred Rule #1** (back up before modifying a
large or important file) is made with one command:

```bash
engineering/tools/backup-file.sh <path>
```

It lands in one place, mirroring the file's repo-relative path with a
timestamp appended:

```
.backups/<repo-relative-path>.<YYYYMMDD-HHMMSS>
```

```
.backups/deliverables/ai/P2/hardware/edge-32mb-module.yaml.20260808-143022
.backups/engineering/operations/P2KB-CORRECTION-FINDINGS.md.20260808-143515
```

**Do not hand-name backups.** Do not add per-file backup rules to
`.gitignore`. The script and the single ignore rule cover every case.

Other commands:

```bash
engineering/tools/backup-file.sh --list         # what is currently held
engineering/tools/backup-file.sh --prune 30     # delete backups older than N days
```

---

## Why a sidecar directory rather than a suffix

**Backups must not sit beside the file they copy.** A backup adjacent to its
original is reachable by every `grep`, glob, `find`, audit script, and
source-selection step in the workspace — and it looks exactly like the real
thing.

This is not hypothetical. Backup copies of the DeSilva opus-masters were
mistaken for the live source; the same class of error recurred during the
2026-08-08 census itself, when an audit sweep reported
`edge-32mb-module.yaml.backup-20250108` as a live shipped YAML. Moving
backups out of the tree makes that failure structurally impossible instead of
something each script has to remember to exclude.

The secondary benefit is that one ignore rule can never drift. The convention
this replaced had **eight naming shapes** — `.backup.YYYYMMDD_HHMMSS`,
`.backup-YYYYMMDD-HHMMSS`, `.backup-YYYYMMDD`, `.bak`,
`.pre-merge-backup.<ts>`, `.backup-<reason>`, `-OLD.<ext>`, and
`SESSION-END-BACKUP-*.md` — which required **fifteen** `.gitignore` rules to
contain, three of them naming individual files by hand. Every new shape meant
another rule. A directory cannot be gotten wrong: anything inside it is
ignored regardless of what it is named.

---

## Never back up a regenerable artifact

If a generator can rebuild the file, **the generator is the backup**. Do not
copy:

- workspace renders (`document-production/workspace/**`) — rebuilt from
  `opus-master/` by `prepare-manual` on every run
- generated indexes and AI-reference output — rebuilt by the index generator
- extracted text / converted source — rebuilt from the source document

In the 2026-08-08 census, **222 of 354** loose backups were copies of
workspace renders: files that were already reproducible. This one rule
eliminates roughly two-thirds of backup volume at the source.

---

## Retention

For a **tracked** file, git history is the real backup. These copies only
guard the window between an edit and its commit, so they are cheap to discard
— prune at 30 days without ceremony.

For an **untracked** file, the backup is the only copy. Prune with care, and
prefer promoting anything genuinely worth keeping into a deliberate archive
(below) rather than leaving it in `.backups/`.

---

## Backups are not archives

Two different things, and the distinction is what keeps a cleanup sweep from
destroying deliberate work:

| | Backup | Archive |
|---|---|---|
| **Created** | mechanically, before an edit | deliberately, when retiring a document |
| **Lives in** | `.backups/` | `archive/` beside the work it retired |
| **Lifetime** | prunable, days-to-weeks | kept as long as it is useful |
| **Swept by cleanup?** | yes | **never** |

Deliberate archives — `DRAFTS/archive/`, `engineering/archive/`,
`engineering/workspace/archived-work/`, per-manual `archive/` folders — have a
job and are **out of scope** for this convention. A sweep keyed on the word
"backup" in a path would delete them; a sweep keyed on *how the file was
created* does not.

---

## Migration record (2026-08-08)

- **532 files / 57 MB** relocated from the working tree into `.backups/`,
  preserving repo-relative paths. Nothing deleted — all were untracked and
  gitignored, so deletion would have been unrecoverable.
- **15 `.gitignore` rules → 1** authoritative rule plus a small defensive net
  for backups made by other tools (editors, `sed -i.bak`, `patch`).
- **Deliberately left in place**, pending a decision on where they belong:
  - `engineering/pipelines/backups/` (2 files)
  - `engineering/document-production/pipelines/backups/` (1 file,
    `pdf-generation-guide-RECOVERED.md.backup.20250820_212847`)

  These are dated 2025-08-20/21 and one is named *RECOVERED* — they appear to
  be the salvaged artifacts of the 3300-line documentation loss that created
  Sacred Rule #1. They deserve a deliberate archive, not a prune.
- **Left tracked**, needing a separate decision (moving tracked content is a
  repo change, not clutter removal):
  - `engineering/history/sessions/SESSION-END-BACKUP-20250825.md` — reads as a
    session history document that merely has "BACKUP" in its name
  - `.../p2-pasm-desilva-style/opus-master/COMPLETE-OPUS-MASTER-backup-2025-12-06-pre-backport.md`
    — tracked, and sitting in the DeSilva master folder: exactly the adjacency
    this convention exists to prevent. Git already preserves its content, so
    it can be removed from the tree safely whenever that call is made.
