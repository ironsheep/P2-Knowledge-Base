# About Document Production

*Methodology & orientation for P2 documentation generation. For current
publication status see [`README.md`](README.md); the authoritative state of every
document is [`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md).*

---

## Production philosophy

We create professional technical documentation optimized for both human learning
and AI consumption. Every document flows through one systematic pipeline so that
accuracy, typography, and structure stay consistent across the whole library — and
so a fix made once propagates everywhere it applies.

Quality is paramount: every release raises quality, never lowers it. Hallucinations
happen at the moment of writing, so we verify against primary sources *before*
writing and audit again before releasing (see the audit methodology below).

## The document classes

Document production covers four classes, each with its own authoring tree:

| Class | Authoring tree | Examples |
|-------|----------------|----------|
| **Manual** | `manuals/` | Assembly Language Reference, DeSilva Tutorial, Debug Window, Streamer, I/O & Smart Pins |
| **Application note** (`P2ANxxx`) | `app-notes/` | P2AN001 (ADC), P2AN002 (CORDIC) — single-technique, one runnable example, ships a YAML companion |
| **Datasheet** | `datasheets/` | P2-Eval-HUB75-Adapter |
| **Presentation-class** | `manuals/` | AI Privacy Guide (rides pristine foundation, not the shared content stack) |

All are categorized exactly once in [`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md),
which drives both consistency scope (the live set must stay mutually consistent) and
how the `whats-next` skill resumes work.

## The Three-Folder Rule

Every official document has three parallel folders sharing one canonical name:

```
<authoring-tree>/<name>/   ← CONTENT AUTHORING (authoritative — opus-master/)
workspace/<name>/          ← PRODUCTION PREPARATION (generated; never hand-edited)
outbound/<name>/           ← STAGING FOR PDF FORGE (only changed files)
```

**Edit the opus-master, never the workspace render** — the workspace is regenerated
from the master and overwrites edits. Full detail:
[`PDF-PRODUCTION-ARCHITECTURE.md`](PDF-PRODUCTION-ARCHITECTURE.md).

## The shared platform stack

All live technical publications ride one shared **`p2kb-platform-*`** display stack
(`platform/`): a foundation layer, a shared content layer
(`p2kb-platform-content.sty` — the code-box family, callouts), and shared Lua filters
(code-coloring, mnemonic styling, cross-references, pagination, figures). This
replaced the old per-document forks: a typography or convention change is made once
in `platform/` and every consuming manual picks it up on its next render.

Because the manuals share one stack, a PDF goes stale the moment a platform file it
consumes changes after that PDF was built — the **Platform Freshness Ledger** in the
roster is the detector. The cross-publication conventions that must stay consistent
(code-block color = language, geometry, fonts) are defined in the roster's *Shared
conventions* section.

## The skill-driven workflow

Production is driven by skills rather than ad-hoc steps:

| Stage | Skill | Does |
|-------|-------|------|
| Resume | `whats-next` | head-aware session front door; reads `active_element`, resolves standing state |
| Audit | `document-audit` | audit a manual against the current YAML/KB HEAD + itself; enforces the publish gate |
| Finalize | `document-finalize` | gather all findings → fix in rework-safe order → render once |
| Prepare | `prepare-manual` | refresh workspace from opus-master, escape LaTeX, stage only changed files to outbound |
| Generate | *(PDF Forge)* | Stephen deploys the outbound bundle; the Forge produces the PDF |
| Release | `release-manual` | verify the PDF is complete, promote CHANGELOG, update the deliverables index, record the ledger |

PDFs are produced **only on PDF Forge** (never local pandoc). The interactive
`forge-test` daemon is for nailing down template/layout behavior; production
deliverables go through `prepare-manual` → Forge.

## Audit methodology (write-time + release-time)

Prevention beats detection, but both are required:

- **Write-time** — verify each claim against primary sources (the P2KB YAML, the
  Silicon Doc, hardware-verified findings) before writing it.
- **Release-time** — `document-audit` builds a truth matrix, extracts claims,
  cross-references each, and classifies VERIFIED / MODIFIED / UNVERIFIED /
  FABRICATED. The publish gate blocks release while actionable YAML corrections are
  pending.

Per-manual specifics (sources, code-line budget K, doc class, fragile areas) live in
each manual's `MANUAL-DESCRIPTOR.md` overlay.

## Deeper references

- [`PDF-PRODUCTION-ARCHITECTURE.md`](PDF-PRODUCTION-ARCHITECTURE.md) — file layout & content flow (read first for PDF work)
- [`methodology/`](methodology/) — the deep process docs (generation, layout standards, example-library mechanism, stylesheet architecture)
- [`standards/`](standards/) — front-matter & code-coloring standards
- [`TEMPLATE-CATALOG.md`](TEMPLATE-CATALOG.md) — the template inventory
- [`PUNCH-LIST.md`](PUNCH-LIST.md) — cross-cutting cleanup / technical debt

---

*This document explains our production methodology. For current pipeline status, see
[`README.md`](README.md); for the authoritative per-document state, see
[`PUBLICATION-ROSTER.md`](PUBLICATION-ROSTER.md).*
