# PDF Production Architecture

**Purpose**: Central reference for PDF document production workflow - where files live, where edits happen, how content flows to PDF Forge.

**Read this FIRST** when starting PDF work. Then read the document-specific Quick Guide.

---

## The Three-Folder Rule

Every official document has three parallel folders with the **same canonical name**:

```
<authoring-tree>/[doc-name]/   ← CONTENT AUTHORING (authoritative)
workspace/[doc-name]/          ← PRODUCTION PREPARATION
outbound/[doc-name]/           ← STAGING FOR PDF FORGE
```

**All three document classes use this same rule** — only the authoring tree differs:

| Class | Authoring tree (`<authoring-tree>/`) | Example doc-name |
|-------|--------------------------------------|------------------|
| Manual | `manuals/` | `p2-streamer-programming-guide` |
| Application note | `app-notes/` | `P2AN001` |
| Datasheet | `datasheets/` | `P2-Eval-HUB75-Adapter-Datasheet` |

`workspace/` and `outbound/` are **single flat trees keyed by doc-name**, shared
across all three classes — which is what makes the production tooling
(`prepare-manual` / `release-manual` / `forge-test`) document-class-agnostic: it
resolves the three folders by canonical name regardless of class. An app note or
datasheet enters production by gaining `workspace/<name>/` + `outbound/<name>/`
entries, exactly as a manual does. A doc whose opus-master lives outside `manuals/`
bridges to the shared workspace via its `assemble-manual.sh` (whose `OPUS_MASTER`
path points into the right authoring tree). App notes additionally use the shared
`p2kb-platform-*` stack with a thin `p2kb-appnote-*` class layer (cover keeps the
family artwork; the manuals' Parts/Chapters cover box is repurposed to an app-note
"What You'll Build" box). P2AN001 is the pilot (2026-06-28).

**Canonical names** are established when a document is created and never change
(e.g. `p2-assembly-language-manual`, `p2-pasm-desilva-style`).

**The list of documents and their statuses lives in exactly one place:
[`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md).** Do not restate it here. Every
manual-shaped folder appears in the roster exactly once, under its lifecycle status
(Done / In progress / Upcoming / Abandoned) and with its Type — that is the authority
a sweep consults, and a second copy in this file is how the two drift apart.

---

## Where Edits Happen - THE CARDINAL RULE

| Edit Type | Location | Never Edit In |
|-----------|----------|---------------|
| **Content changes** | `manuals/[doc]/opus-master/` | workspace/ or outbound/ |
| **Template/style changes** | `workspace/[doc]/templates/` | outbound/ |
| **Lua filter changes** | `workspace/[doc]/filters/` | outbound/ |
| **Request config** | `workspace/[doc]/request.json` | outbound/ |

**Why this matters**:
- `manuals/opus-master/` is the authoritative source. Editing workspace copies causes double-work.
- `outbound/` is staging only - files get moved to Forge and disappear.

---

## Directory Structure

```
engineering/document-production/
├── manuals/
│   └── [doc-name]/
│       ├── opus-master/           ← AUTHORITATIVE CONTENT
│       │   ├── front-matter.md
│       │   ├── chapter-01.md
│       │   └── ...
│       ├── creation-guide.md      ← Document requirements
│       ├── voice-guide.md         ← Writing voice/tone
│       └── style-guide.md         ← Visual style decisions
│
├── workspace/
│   └── [doc-name]/
│       ├── [Document].md          ← Assembled from opus-master
│       ├── templates/
│       │   ├── p2kb-[short].latex
│       │   └── p2kb-[short]-*.sty
│       ├── filters/
│       │   └── *.lua
│       ├── request.json
│       ├── request-requirements.json
│       └── README.md              ← Workspace-specific instructions
│
└── outbound/
    └── [doc-name]/                ← FLAT structure for PDF Forge
        ├── [Document].md          ← ESCAPED copy
        ├── *.latex                ← Templates at root (no subdirs!)
        ├── *.sty
        ├── *.lua
        └── request.json
```

---

## Content Flow

```
manuals/opus-master/     →    workspace/           →    outbound/         →  PDF Forge
(write content here)         (assemble & prepare)      (escape & stage)      (generate)
```

**Step by step**:
1. **Author** content in `manuals/[doc]/opus-master/`
2. **Assemble** into single document in `workspace/[doc]/`
3. **Escape** LaTeX characters and copy to `outbound/[doc]/` (flat!)
4. **User deploys** outbound files to PDF Forge
5. **Review** generated PDF, fix issues in manuals/ or workspace/, repeat

---

## Two Operational Modes

### Interactive Testing (Claude-driven)

**When to use**: Debugging templates, rapid visual iteration, testing Lua filters

**Location**: `engineering/pdf-forge/interactive-testing/`

**How it works**:
- Directory syncs directly to PDF Forge's `/workspace/shared/`
- Claude drops test requests, reads results automatically
- No human intervention needed once Forge listener is running
- Fast feedback cycles (30-60 seconds)

**Guide**: `engineering/pdf-forge/work-modes/automated-pdf-testing.md`

### Production Generation (User-deployed)

**When to use**: Final deliverables, release documents, quality-verified output

**Location**: `engineering/document-production/outbound/[doc-name]/`

**How it works**:
- Claude prepares files in outbound (escaped, flat structure)
- User hand-copies to PDF Forge
- Longer cycles but controlled deployment

**Guide**: `engineering/pdf-forge/work-modes/production-pdf-generation.md`

---

## File Naming Conventions

### Document Files
- Master document name is **sacred** - never add suffixes
- Same filename in workspace AND outbound: `P2-Assembly-Language-Manual.md`
- No `-escaped`, `-v2`, `-final`, `-working` suffixes

### Template Files
- Pattern: `p2kb-[short-name].latex` (main template)
- Pattern: `p2kb-[short-name]-[purpose].sty` (style packages)
- Short name appears in all related files: `p2kb-pasm2-*.sty`

### Request Files
- Always `request.json` - never rename
- `request-requirements.json` for mandatory pandoc args

---

## New Document Startup Checklist

When creating a brand new manual, follow this sequence:

### 1. Establish Identity
- [ ] Choose **canonical name** (lowercase, hyphenated): `p2-[topic]-manual` or `p2-[topic]-tutorial`
- [ ] Define **document title** (human-readable)
- [ ] Determine **short name** for templates: `pasm2`, `smart-pins`, `desilva`, etc.

### 2. Create Three Parallel Folders
```bash
mkdir -p engineering/document-production/manuals/[canonical-name]/opus-master
mkdir -p engineering/document-production/workspace/[canonical-name]/templates
mkdir -p engineering/document-production/workspace/[canonical-name]/filters
mkdir -p engineering/document-production/outbound/[canonical-name]
```

### 3. Create Foundation Documents (in manuals/)
- [ ] `creation-guide.md` - Document requirements, scope, audience, structure
- [ ] `voice-guide.md` - Writing voice/tone for this document
- [ ] `style-guide.md` - Visual style decisions (if different from standard)

### 4. Create Workspace Infrastructure
- [ ] `workspace/[name]/README.md` - Copy from existing workspace README, adapt
- [ ] `workspace/[name]/request.json` - PDF Forge configuration
- [ ] `workspace/[name]/request-requirements.json` - Mandatory pandoc args (if needed)
- [ ] `workspace/[name]/templates/p2kb-[short].latex` - Main template
- [ ] `workspace/[name]/templates/p2kb-[short]-*.sty` - Style packages

### 5. Begin Content Authoring
- [ ] Create chapter files in `manuals/[name]/opus-master/`
- [ ] Use Opus model for initial content generation
- [ ] Follow creation-guide requirements

### 6. Update Tracking
- [ ] Add to "Active Documents Status" table below
- [ ] Add document-specific Quick Guide if complex workflow needed

---

## Publication: Releasing to Community

When a document is ready for community review and use:

### 1. User Places PDF in Deliverables
```
deliverables/documents/[Document-Name].pdf
```
This is a **manual step** - user copies the final PDF from PDF Forge output.

### 2. Claude Updates README
Update `deliverables/documents/README.md`:
- **Move** the document from "Coming soon" to "Available Documents"
- Add title, subtitle, version/date
- Add brief description of purpose/audience
- Add link to the PDF file

**Example entry** (in Available Documents section):
```markdown
### [P2 Assembly Language Reference Manual](P2-Assembly-Language-Manual.pdf)
**Version**: 1.0 (December 2025)
Complete PASM2 instruction set documentation for experienced P2 developers.
Covers all 359 instructions, directives, and special registers.
```

### 3. Document Lifecycle Complete
```
Development          Production           Publication
─────────────────────────────────────────────────────────
manuals/opus-master  →  workspace/  →  outbound/  →  PDF Forge
                                                        ↓
                                          deliverables/documents/
                                                        ↓
                                              README.md updated
```

---

## Active Documents Status

**This table used to enumerate the documents and their statuses. It no longer does** —
that enumeration is [`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md)'s job, and keeping a
second copy here is precisely how this file came to list a retired document as `Active`.

What belongs here is the *shape* every document follows, not which documents exist:

| Tree | Holds | Who writes it |
|------|-------|---------------|
| `manuals/<name>/` | `opus-master/` (canonical content), `audit/`, `CHANGELOG.md`, the creation and voice guides | authored by hand — this is the source of truth for content |
| `workspace/<name>/` | the assembled render input, templates, filters, assets | regenerated from `opus-master/` by `prepare-manual`; never hand-edited |
| `outbound/<name>/` | only the files that changed this session | staged for the Forge, which persists everything by filename |

A document may legitimately have a `workspace/` with no `manuals/` (a utility doc or a
placeholder). Look it up in the roster rather than inferring status from which folders exist.

---

## Quick Reference: What Goes Where

| I need to... | Go to... |
|--------------|----------|
| Edit document content | `manuals/[doc]/opus-master/` |
| Edit templates or styles | `workspace/[doc]/templates/` |
| Edit Lua filters | `workspace/[doc]/filters/` |
| Stage for production | `outbound/[doc]/` (flat, escaped) |
| Run interactive tests | `pdf-forge/interactive-testing/` |
| Check document requirements | `manuals/[doc]/creation-guide.md` |
| Check workspace setup | `workspace/[doc]/README.md` |

---

## Related Documents

| Document | Purpose |
|----------|---------|
| `PDF-CLAUDE-RULES.md` | Don'ts and gotchas for Claude |
| `production-pdf-generation.md` | Production mode workflow |
| `automated-pdf-testing.md` | Interactive testing workflow |
| `PRODUCTION-REQUEST-FORMAT.md` | request.json format reference |
| Individual `workspace/[doc]/README.md` | Document-specific instructions |

---

*This is the central reference for PDF production. Read document-specific guides after understanding this architecture.*
