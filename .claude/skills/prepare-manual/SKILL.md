---
name: prepare-manual
description: Prepare a P2 manual for PDF Forge generation — refresh workspace from opus-master, escape LaTeX characters, and stage only changed files to outbound. Use when the user says "prepare/build/stage the <manual> for PDF", "get <manual> ready for the Forge", or invokes /prepare-manual. Works for any manual under engineering/document-production/workspace/. Does NOT generate the PDF itself (PDF Forge does that); produces the outbound bundle that the user moves to Forge.
---

# Prepare Manual for PDF Forge

You are preparing a P2 manual for deployment to PDF Forge. The skill is **document-agnostic** — it discovers per-manual conventions from the manual's own `README.md` and `request.json`.

## Repo layout (constant across all manuals)

```
engineering/document-production/
├── manuals/<slug>/              # Canonical source (read-only here)
│   └── opus-master/             # Either a single .md OR a tree of chapter files
├── workspace/<slug>/            # Production prep (unescaped working copy)
│   ├── README.md                # Per-manual conventions — authoritative
│   ├── <DocName>.md             # The working copy (filename from request.json)
│   ├── templates/               # *.latex, *.sty
│   ├── filters/                 # *.lua
│   ├── assets/                  # Optional images
│   ├── request.json             # PDF Forge configuration
│   ├── request-requirements.json
│   └── assemble-manual.sh       # ONLY present for multi-file manuals
└── outbound/<slug>/             # FLAT staging — what user moves to Forge

engineering/tools/conversion/
└── latex-escape-all.sh          # Universal escape script
```

## Sacred rules (do not violate)

- **Sacred Rule #1** — Backup workspace working copy before overwriting it (>50KB or >100 lines). Use `cp <file> <file>.backup.$(date +%Y%m%d_%H%M%S)`.
- **Sacred Rule #6** — Only stage files to outbound that **actually changed**. Forge is persistent and keeps the last version of every file. Sending unchanged files wastes the user's deployment time. The markdown changes every iteration; templates/filters/`request.json` usually do not.
- **Sacred Rule #5** — Never rename files. The working-copy filename in `request.json` is sacred and identical in workspace and outbound.
- Outbound is **FLAT** — no subdirectories for templates/filters. (Assets, if used, do go in `outbound/<slug>/assets/`.)

## Execution plan

### Step 1 — Identify the manual

The user may pass a slug as an argument. If not:
- List subdirectories of `engineering/document-production/workspace/` (exclude `.DS_Store`).
- If exactly one workspace has uncommitted changes per `git status`, suggest that one first.
- Ask the user with `AskUserQuestion` which manual to prepare.

### Step 2 — Read the manual's conventions

In parallel, read these files from `workspace/<slug>/`:
- `README.md` — confirms filename, assembly approach, any special rules
- `request.json` — extract `documents[0].input` (= `<DocName>.md`), `lua_filters`, `metadata.{version,date}`
- `request-requirements.json` (if present) — mandatory pandoc args
- Check whether `workspace/<slug>/assemble-manual.sh` exists (= multi-file manual)

### Step 3 — Detect assembly method

- **Multi-file** — `workspace/<slug>/assemble-manual.sh` exists. Run it from the workspace dir; it concatenates `manuals/<slug>/opus-master/**/*.md` into `workspace/<slug>/<DocName>.md`.
- **Single-file** — Look for `manuals/<slug>/opus-master/<DocName>.md` first, then `COMPLETE-OPUS-MASTER.md`, then the only `.md` file in `opus-master/`. Copy that file → `workspace/<slug>/<DocName>.md`.
- **Ambiguous** — Ask the user.

### Step 4 — Detect what changed

Run these scoped to the manual's workspace:
```bash
git status --porcelain engineering/document-production/workspace/<slug>/
git log -5 --oneline engineering/document-production/manuals/<slug>/opus-master/
```

Classify each modified file:
- `<DocName>.md` — gets refreshed from opus-master in Step 6; ignore for change-detection purposes.
- Files under `templates/` (`.latex`, `.sty`) — candidates for staging.
- Files under `filters/` (`.lua`) — candidates for staging.
- `request.json` — candidate for staging (especially if metadata bumped this session).
- `assets/` — copy if changed; outbound has `assets/` subdir even though the rest is flat.
- Backup files (`*.backup.*`), `.DS_Store`, etc. — ignore.

Also compare opus-master modtime/size to workspace working copy to know if a refresh is needed.

### Step 5 — Present the plan and ask for confirmation

**FIRST**, also check for **hardcoded version/date strings in the markdown source** (the cover page is rendered from the markdown, not from `request.json` metadata — `request.json` metadata only affects PDF properties / headers / footers, not the visible cover):

- **Multi-file manual**: grep `opus-master/front-matter.md` for `Version\|2026\|2025`
- **Single-file manual**: grep the first ~50 lines of `opus-master/<single>.md`

Typical pattern is two LaTeX lines inside a `{=latex}` block: `{\large <Month> <Year>\par}` (date) and `{\large\color{blue}Version <N>\par}` (version). These MUST be updated alongside `request.json` or the PDF's cover will not match the metadata.

Then use `AskUserQuestion` to present:
1. **Refresh source?** — show opus-master vs working-copy diff summary (newer/older/same).
2. **Version bump?** — show CURRENT values in BOTH (a) `request.json` metadata and (b) markdown cover (front-matter file or single-file cover region). If recent commits to opus-master mention a version (e.g., "v2.3.0"), suggest that. Today's month/year as date. Offer: bump both to suggested / keep as-is / custom. Bumping ONE without the other creates a confusing mismatch — flag this risk explicitly if the user wants to do partial.
3. **Files to stage** — list each candidate template/filter/`request.json` with its git status. Offer: stage all / pick a subset / stage none (markdown only).

If the user has clearly signaled "just do it" in this session, you may skip confirmation for unambiguous cases — but always show what you're about to do at minimum.

### Step 6 — Execute

In order (each step depends on the previous):

1. **Backup** workspace working copy if it exists and the assembly will overwrite it:
   ```bash
   cp workspace/<slug>/<DocName>.md workspace/<slug>/<DocName>.md.backup.$(date +%Y%m%d_%H%M%S)
   ```
2. **Apply markdown source edits FIRST** if confirmed in Step 5 (cover-page version/date in `front-matter.md` for multi-file, or cover region of single-file master). Do this BEFORE assembly so the new values flow into the assembled working copy.
3. **Assemble or copy** from opus-master per Step 3. If using `assemble-manual.sh` and it errors with "bad interpreter: Permission denied", run `chmod +x <script>` and retry — the executable bit doesn't always survive across systems.
4. **Apply version bump** to `request.json` if confirmed (use `mcp__filesystem__edit_file`).
5. **Escape** the markdown into outbound:
   ```bash
   cd workspace/<slug>
   ../../../tools/conversion/latex-escape-all.sh \
       <DocName>.md \
       ../../outbound/<slug>/<DocName>.md
   ```
   The escape script creates its own backup of the workspace source — that's expected, harmless.
6. **Stage changed aux files** confirmed in Step 5:
   ```bash
   cp workspace/<slug>/templates/<file> outbound/<slug>/        # FLAT — no templates/ subdir
   cp workspace/<slug>/filters/<file>   outbound/<slug>/        # FLAT — no filters/ subdir
   cp workspace/<slug>/request.json     outbound/<slug>/        # If metadata bumped or filters changed
   ```
   For asset changes: `cp workspace/<slug>/assets/<file> outbound/<slug>/assets/` (the `assets/` subdir IS used in outbound).

### Step 7 — Report

End with a brief summary:
- Final list of files in `outbound/<slug>/` with sizes (`ls -la`).
- Note which aux files were intentionally NOT staged (= Forge already has them).
- Tell user the bundle is ready to move to PDF Forge.
- Mention the auto-backup the escape script created (harmless).

Do not exceed 4-6 lines of report text plus the file table.

## Tool preferences (per CLAUDE.md)

- Filesystem reads/edits/listings → prefer `mcp__filesystem__*` tools (no permission prompts).
- File copies, script execution, `git status`/`git log` → Bash.
- Use `Edit` or `mcp__filesystem__edit_file` for `request.json` (not redirection).

## What this skill does NOT do

- Does not generate the PDF (PDF Forge does that on the user's deploy).
- Does not edit content in `manuals/<slug>/opus-master/` (that's done separately).
- Does not commit anything (user controls git).
- Does not prune `*.backup.*` files in the workspace (separate hygiene task).
- Does not deploy to PDF Forge (user moves files manually).

## Error handling

- If `manuals/<slug>/opus-master/` is missing or empty → stop and report; the source is broken.
- If `workspace/<slug>/request.json` is missing → stop and ask the user to initialize the workspace first.
- If `assemble-manual.sh` exits non-zero → stop, show output, do not stage.
- If escape script errors → stop, show output, do not stage anything else.
- If `git status` shows the working copy was modified by the user (not just opus-master regen) → flag it and ask before overwriting.
