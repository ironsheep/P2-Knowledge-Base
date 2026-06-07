---
name: prepare-manual
description: Prepare a P2 manual for PDF Forge generation — refresh workspace from opus-master, escape LaTeX characters, and stage only changed files to outbound. Use when the user says "prepare/build/stage the <manual> for PDF", "get <manual> ready for the Forge", or invokes /prepare-manual. Works for any manual under engineering/document-production/workspace/. Does NOT generate the PDF itself (PDF Forge does that); produces the outbound bundle that the user moves to Forge.
---

# Prepare Manual for PDF Forge

You are preparing a P2 manual for deployment to PDF Forge. The skill is **document-agnostic** — it discovers per-manual conventions from the manual's own `README.md` and `request.json`.

## Repo layout (constant across all manuals)

```
engineering/document-production/
├── platform/                    # SHARED rendering stack (consumed by many manuals)
│   ├── templates/               # p2kb-platform-{foundation,content}.sty
│   └── filters/                 # p2kb-platform-*.lua
├── manuals/<slug>/              # Canonical source (read-only here)
│   └── opus-master/             # Either a single .md OR a tree of chapter files
├── workspace/<slug>/            # Production prep (unescaped working copy)
│   ├── README.md                # Per-manual conventions — authoritative
│   ├── <DocName>.md             # The working copy (filename from request.json)
│   ├── templates/               # *.latex, *.sty (per-manual: reference.latex, local, diagrams)
│   ├── filters/                 # *.lua (per-manual fork filters, if any)
│   ├── assets/                  # Optional images
│   ├── request.json             # PDF Forge configuration
│   ├── request-requirements.json
│   └── assemble-manual.sh       # ONLY present for multi-file manuals
└── outbound/<slug>/             # FLAT staging — what user moves to Forge

engineering/tools/conversion/
└── latex-escape-all.sh          # Universal escape script
```

**Platform-consuming manuals.** A manual "consumes the platform" when its
`templates/<...>-reference.latex` does `\usepackage{p2kb-platform-foundation}` /
`{p2kb-platform-content}` AND/OR its `request.json` `lua_filters` name
`p2kb-platform-*`. Those shared files live in `platform/`, **not** in the manual's
workspace — but Forge's manual store still needs them, so prepare-manual stages
them from `platform/` too (see the Platform-stack staging rule below). The
unification program is moving every manual onto this model (Streamer is the pilot;
study: `methodology/presentation-platform-unification-STUDY.md`).

## Sacred rules (do not violate)

- **Sacred Rule #1** — Backup workspace working copy before overwriting it (>50KB or >100 lines). Use `cp <file> <file>.backup.$(date +%Y%m%d_%H%M%S)`.
- **Sacred Rule #6** — Only stage files to outbound that **actually changed** (vs. what Forge already holds). Sending unchanged files wastes the user's deployment time. The markdown changes every iteration; templates/filters/`request.json` usually do not.
- **How PDF Forge persistence works (the mental model).** When the user moves outbound → Forge, the files are **removed from outbound**. Outbound going empty after a deploy is **expected, not an error** — never treat a previously-staged file's absence from outbound as a problem. Forge then **retains the last-moved version of each file, keyed by filename, until that filename is overwritten.** Consequence: files with **unique per-document names** (e.g. the streamer's `templates/*` and `filters/p2kb-streamer-*`) accumulate on Forge and survive across documents — stage them only on the first build of a document or when they change. But **`request.json` has the SAME filename for every manual**, so Forge only ever holds ONE — whichever document was deployed last.
  - **Forge has TWO COMPLETELY SEPARATE file stores: the manual-PDF-generation store and the interactive/daemon store.** This prepare-manual → outbound → manual-PDF-generation path feeds ONLY the **manual store**. The `forge-test` interactive daemon feeds ONLY the **interactive store**. A file sent to one does **not** appear in the other — there is no shared store. To make any file appear in the manual store, it MUST travel the manual PDF generation process. The keyed-by-filename persistence rule (above) holds *within each store independently*.
  - **Consequence — "changed since Forge last had it" means "since the MANUAL store last had it," not since the last daemon render.** Templates/filters iterated and verified via the daemon are NOT in the manual store; they must be staged through outbound to reach it. So the FIRST time a document goes through the manual PDF generation process, the manual store has NONE of its files → **stage the COMPLETE stack** (all templates + all filters + request.json + md), even though they were "already on Forge" via the daemon. On subsequent manual builds, stage only what changed *since the last manual build* (the daemon's separate history is irrelevant to the manual store).
- **Platform-stack staging rule (shared files, shared names).** For a
  platform-consuming manual (see above), the platform `.sty` its `reference.latex`
  loads (`platform/templates/p2kb-platform-*.sty`) and the platform `.lua` named in
  its `request.json` (`platform/filters/p2kb-platform-*.lua`) are part of the stack
  Forge must hold — but they are NOT under `workspace/<slug>/`, so they need explicit
  staging from `platform/`. Because every manual ships these under the SAME filenames,
  the manual store holds ONE copy each, keyed by filename — so seeding is **global**,
  tracked in todo-mcp key `manual_store_platform_seeded` (NOT per-slug). Stage the
  platform files this manual uses when **either**: (a) `manual_store_platform_seeded`
  is unset (the manual store has no platform files yet — first platform-consuming
  build ever), **or** (b) `git status --porcelain engineering/document-production/platform/`
  shows the platform files changed (a platform fix must reach Forge). Otherwise the
  manual store already has the current platform bytes — do NOT re-stage them (Sacred
  Rule #6). After staging, set `manual_store_platform_seeded` (Step 7). Note: because
  the flag is global, a platform CHANGE must re-stage for whichever manual is built
  next — rely on the git-status signal (b), not just the flag, to catch that.
- **Document-switch override — ALWAYS stage `request.json` when switching documents.** Because `request.json` shares one filename across all manuals (previous point), Forge's copy is for the *previous* document — its directive (input, template, lua_filters, metadata) points at the wrong manual. So whenever the manual you are preparing differs from the one prepared last time, you MUST stage `request.json` to outbound **even though git shows it unchanged**. This is the one sanctioned exception to Sacred Rule #6. Track the last-prepared manual in todo-mcp context key `pdf_forge_last_prepared_manual`; compare it to the current slug in Step 4, force-stage `request.json` on a mismatch (or when the key is absent), and update the key in Step 7. (On a *first-ever* build of a document, also stage its uniquely-named templates/filters — Forge does not have them yet.)
- **A `.tex` file appearing in outbound is a layout-debug hand-back — NOT a staging artifact.** When a PDF has a gnarly layout problem, the user occasionally takes the **`.tex`** that PDF Forge emits during generation (the Pandoc-produced LaTeX, before xelatex makes the PDF) and drops it **back into `outbound/<slug>/`** for inspection. If you see a `.tex` there, it is the actual generated LaTeX for you to **read and diagnose** the layout issue against the template/filters — do NOT delete it, overwrite it, escape it, or treat it as something to send to Forge. Leave it in place and use it; it is inbound-for-debugging, not outbound-for-deploy.
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

**Document-switch check (decides `request.json` staging).** Read the todo-mcp context key `pdf_forge_last_prepared_manual`. If it is **absent or differs** from the current `<slug>`, this is a **document switch** — `request.json` MUST be staged in Step 6 regardless of its git status, because Forge still holds the previous document's directive (wrong template/filters/input). If it **equals** the current slug, stage `request.json` only if it actually changed this session.

**Manual-store-seeded check (decides whether the FULL stack may be staged).** The "first manual build → stage the complete stack" clause (templates + filters + request.json + md) applies ONLY when the **manual** PDF-generation store is genuinely empty for this document. Determine seeded-ness from concrete signals, not memory:
- todo-mcp context key `manual_store_seeded_<slug>` is set, **OR**
- a previously manually-generated PDF exists for this document (e.g. in `deliverables/.../DOCs/` or wherever this manual's PDF lands).

If **either** signal is true, the manual store already holds this document's full stack → **stage ONLY the files that changed since the last manual build.** Do NOT re-stage unchanged templates/filters — that is the Sacred Rule #6 violation. (Tell: re-copying the whole `p2kb-<slug>-*` stack when only a few files changed. Iterating templates/filters via the `forge-test` daemon does NOT seed the manual store — daemon history is irrelevant here.) Treat a build as first-only when BOTH signals are false.

**Platform-stack check (decides whether the shared `platform/` files stage).** If this manual consumes the platform (its `reference.latex` loads `p2kb-platform-*` or its `request.json` names `p2kb-platform-*` filters), determine whether the shared files must stage per the **Platform-stack staging rule** above:
```bash
git status --porcelain engineering/document-production/platform/   # (b) platform changed?
mcp__todo-mcp__context_get key:"manual_store_platform_seeded"      # (a) ever seeded?
```
Stage the platform `.sty`/`.lua` this manual uses when the key is unset **or** the git status is non-empty. Resolve WHICH platform files: grep the manual's `reference.latex` for `\usepackage{p2kb-platform-...}` (→ `platform/templates/*.sty`) and read the `p2kb-platform-*` entries in `request.json` `lua_filters` (→ `platform/filters/*.lua`).

### Step 5 — Present the plan and ask for confirmation

**FIRST**, also check for **hardcoded version/date strings in the markdown source** (the cover page is rendered from the markdown, not from `request.json` metadata — `request.json` metadata only affects PDF properties / headers / footers, not the visible cover):

- **Multi-file manual**: grep `opus-master/front-matter.md` for `Version\|2026\|2025`
- **Single-file manual**: grep the first ~50 lines of `opus-master/<single>.md`

Typical pattern is two LaTeX lines inside a `{=latex}` block: `{\large <Month> <Year>\par}` (date) and `{\large\color{blue}Version <N>\par}` (version). These MUST be updated alongside `request.json` or the PDF's cover will not match the metadata.

Then use `AskUserQuestion` to present:
1. **Refresh source?** — show opus-master vs working-copy diff summary (newer/older/same).
2. **Version bump?** — show CURRENT values in BOTH (a) `request.json` metadata and (b) markdown cover (front-matter file or single-file cover region). If recent commits to opus-master mention a version (e.g., "v2.3.0"), suggest that. Today's month/year as date. Offer: bump both to suggested / keep as-is / custom. Bumping ONE without the other creates a confusing mismatch — flag this risk explicitly if the user wants to do partial.
3. **Files to stage** — list each candidate template/filter/`request.json` with its git status, PLUS any shared `platform/` files flagged by the Step-4 Platform-stack check. **Gate the offer on the Step-4 manual-store-seeded check:** if the store is seeded (key set OR a manual PDF already exists), offer ONLY the files that changed this session — do NOT offer "stage the full stack." Offer the complete stack ONLY on a genuine first manual build (both signals false). The platform files follow their OWN gate (global platform-seeded flag + platform git status), independent of the per-manual seeded check. Default: stage just the changed aux files + the markdown (+ platform files if their gate fires).

If the user has clearly signaled "just do it" in this session, you may skip confirmation for unambiguous cases — but always show what you're about to do at minimum.

### Step 6 — Execute

In order (each step depends on the previous):

1. **Backup** workspace working copy if it exists and the assembly will overwrite it:
   ```bash
   cp workspace/<slug>/<DocName>.md workspace/<slug>/<DocName>.md.backup.$(date +%Y%m%d_%H%M%S)
   ```
2. **Apply markdown source edits FIRST** if confirmed in Step 5 (cover-page version/date in `front-matter.md` for multi-file, or cover region of single-file master). Do this BEFORE assembly so the new values flow into the assembled working copy.
3. **Assemble or copy** from opus-master per Step 3. If using `assemble-manual.sh` and it errors with "bad interpreter: Permission denied", run `chmod +x <script>` and retry — the executable bit doesn't always survive across systems.
4. **Code line-length gate.** Code boxes do NOT wrap, so an over-long code line is an authorship defect, not a template concern. Audit the **opus-master source** (so the reported `file:line` points at what the author edits — pass the single master file, or the chapter tree for a multi-file manual) against the manual's calibrated column budget K:
   ```bash
   # single-file: manuals/<slug>/opus-master/<DocName>.md
   # multi-file:  manuals/<slug>/opus-master/**/*.md  (the audit accepts many files)
   python3 engineering/tools/validation/audit-code-line-length.py \
       engineering/document-production/manuals/<slug>/opus-master/<DocName>.md
   ```
   It reads K from `manuals/<slug>/creation-guide.md` (the `**Max code columns (K): N**` line).
   - **Clean (exit 0)** — proceed.
   - **EXEMPT (exit 0, "EXEMPT (instrument)" banner)** — an **instrument** doc (e.g. the layout torture test) whose creation-guide carries a `Code-line gate: EXEMPT (instrument)` line deliberately holds over-budget lines as fixtures (the case-2.2 ruler, the ProcessBox demo). The audit lists them for information but does NOT fail. **Proceed** — do not "fix" those lines; they are the test fixture. (Only a doc explicitly tagged exempt gets this; every real manual still gates on exit 1.)
   - **Violations (exit 1)** — STOP. Relay the located `file:line: cols` list; the lines must be shortened in **opus-master** source before staging, by one of the sanctioned fixes: for a **comment** overflow, either (a) move the comment to full line(s) **above** the instruction at its indent, or (b) **split** it — keep the first part inline and put the overflow on the next line as a comment whose `'` is aligned to the same column as the inline `'` above it; for a **code** overflow, break at a logical boundary with the legal Spin2 `...` line-continuation (or aggregate into a named CON). Never a typeset wrap. Re-assemble and re-run. Do not escape/stage with violations outstanding.
   - **No budget yet (exit 2)** — this manual's K is not calibrated. STOP and calibrate first: if the manual forks the shared code-box stack (page margins `left/right=1in`, `IOSPBlock left=30pt,right=10pt`, identical code `Verbatim`) it **inherits the platform K** (see `manuals/p2-layout-torture-test/creation-guide.md` → Code Line Budget); otherwise measure it with the case-2.2 column ruler on a test render. Add a `## Code Line Budget` section (with the tagged `**Max code columns (K): N**` line + provenance) to the manual's creation-guide, then re-run.
5. **Code compile-certification gate.** These manuals **certify** runnable code, not just eyeball it. A code example that is *runnable* — a complete object/program, or a self-contained block — MUST compile clean with `pnut-ts` before staging:
   ```bash
   pnut-ts -q <example>.spin2     # exit 0 = clean; relay any error with file:line
   ```
   - **Runnable example fails** → STOP, fix in **opus-master** source, re-run. Never stage runnable code that does not compile.
   - **Illustrative fragment** (a single line, or a block that references out-of-scope symbols defined in the surrounding program) → not standalone-compilable by design; certify it is *syntactically* valid (wrap it minimally and compile if in doubt). A long line is shortened with the **legal Spin2 line continuation `...`** at a logical boundary (verified: compiles to the identical value — confirm via the P2KB MCP / a `pnut-ts` round-trip) or, for a comment overflow, by **moving the comment above** the instruction OR **splitting it** with the continuation comment aligned to the inline `'` column — **never** by a typeset wrap.
   - This gate is the compile half of code quality; Step 4 is the width half. Both pass before staging.
6. **Apply version bump** to `request.json` if confirmed (use `mcp__filesystem__edit_file`).
7. **Escape** the markdown into outbound:
   ```bash
   cd workspace/<slug>
   ../../../tools/conversion/latex-escape-all.sh \
       <DocName>.md \
       ../../outbound/<slug>/<DocName>.md
   ```
   The escape script creates its own backup of the workspace source — that's expected, harmless.
8. **Stage changed aux files** confirmed in Step 5:
   ```bash
   cp workspace/<slug>/templates/<file> outbound/<slug>/        # FLAT — no templates/ subdir
   cp workspace/<slug>/filters/<file>   outbound/<slug>/        # FLAT — no filters/ subdir
   cp workspace/<slug>/request.json     outbound/<slug>/        # If metadata bumped, filters changed, OR a document switch (Step 4)
   ```
   **Always** run that `request.json` copy on a document switch (the Step 4 check), even with no git change — otherwise Forge builds with the previous document's directive.
   For asset changes: `cp workspace/<slug>/assets/<file> outbound/<slug>/assets/` (the `assets/` subdir IS used in outbound).
9. **Stage the shared platform files** (only if the Step-4 Platform-stack check said to — first platform-seed OR platform changed). These come from `platform/`, FLAT into outbound, same as any other `.sty`/`.lua`:
   ```bash
   cp engineering/document-production/platform/templates/p2kb-platform-foundation.sty outbound/<slug>/
   cp engineering/document-production/platform/templates/p2kb-platform-content.sty    outbound/<slug>/
   cp engineering/document-production/platform/filters/p2kb-platform-<name>.lua       outbound/<slug>/   # each platform filter in request.json
   ```
   Stage only the platform files THIS manual actually uses (resolved in Step 4). If the check said the manual store already holds the current platform bytes, skip this — do not re-stage (Sacred Rule #6).

### Step 7 — Report (and update the document tracker)

**Update the last-prepared tracker** so the next run can detect a switch:
`mcp__todo-mcp__context_set key:"pdf_forge_last_prepared_manual" value:"<slug>"`.

**Set the manual-store-seeded flag** so future runs know the full stack is already on Forge and stage only changes:
`mcp__todo-mcp__context_set key:"manual_store_seeded_<slug>" value:"true"`.

**If platform files were staged this run, set the global platform-seeded flag:**
`mcp__todo-mcp__context_set key:"manual_store_platform_seeded" value:"true"`. (Leave it set on later runs; a platform CHANGE re-stages via the git-status signal, not this flag.)

End with a brief summary:
- Final list of files in `outbound/<slug>/` with sizes (`ls -la`).
- Note which aux files were intentionally NOT staged (= Forge already has them).
- If this was a document switch, say so and confirm `request.json` was force-staged.
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
