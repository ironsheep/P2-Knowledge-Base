# P2 Errata — Workspace

PDF-production workspace for P2 Errata. The template stack is the shared
`p2kb-platform-*` family (front matter, code-block coloring, reference blocks) per
`engineering/document-production/standards/manual-front-matter-and-code-coloring-standard.md`.
This manual is a **twin** that consumes the platform stack with a thin local override.

## Source of truth

The canonical content lives in the manual's `opus-master/`, NOT in this workspace:

```
../../manuals/p2-errata/opus-master/
  ├── front-matter.md                      # cover, contents, licence, classes, summary table
  ├── e1-setq-block-pointer-step.md         # Chapter 1 = erratum E1
  ├── e2-altx-takes-pending-augs.md         # Chapter 2 = E2
  ├── e3-getct-stale-upper-long.md          # Chapter 3 = E3
  ├── e4-getxacc-clear-gating.md            # Chapter 4 = E4
  ├── e5-goertzel-one-clock-lag.md          # Chapter 5 = E5
  └── appendix-a-test-programs.md           # Appendix A
```

`assemble-manual.sh` concatenates them, in that order, into the workspace
`P2-Errata.md`. **Chapter N is erratum EN, and erratum numbers are permanent**: a new
erratum is appended as the next chapter file and the next line of `REQUIRED_FILES`.

## Three-stage pipeline

1. **Edit** `opus-master/*.md` (canonical source)
2. **Assemble + escape** here: `bash assemble-manual.sh`, then `latex-escape-all.sh` (the `prepare-manual` skill does both)
3. **Stage CHANGED files only** to `../../outbound/p2-errata/` for PDF Forge

The master filename `P2-Errata.md` is sacred — never rename or suffix it.

## Template stack

| File | Role |
|------|------|
| `templates/p2kb-errata-reference.latex` | Main template (11pt book, loads platform foundation + content, then the local) |
| `templates/p2kb-errata-local.sty` | Per-manual override (thin — empty for this twin) |
| `request.json` | PDF Forge build request — references the **platform** lua filters by name (already on the Forge) |

No diagrams package: this manual has no TikZ figures at v0.1.0.

The shared `p2kb-platform-{foundation,content}.sty` and the `p2kb-platform-*.lua`
filters are NOT in this workspace — the Forge already holds them from the rest of the
manual family.

## Document Status

| Item | Status |
|------|--------|
| Content grounding (bench ledger + P2 Documentation) | per-chapter sidecars in `../../manuals/p2-errata/audit/verification/` |
| Template stack (twin on platform) | **Complete** |
| Front matter (house standard) | **Complete**, with a *Community Review Draft* line on the cover |
| First Forge build (v0.1.0 community review draft) | in progress |

## Notes for first build

- Single-image cover `assets/book-artwork.png` — identical md5 across the manual family.
- **First build of this manual on the Forge's manual store**: stage the two templates, the
  cover, and `P2-Errata.md`. The platform files are already there.
