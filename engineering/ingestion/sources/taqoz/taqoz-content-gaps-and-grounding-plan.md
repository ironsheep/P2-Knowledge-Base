# TAQOZ Forth / ROM Monitor — Content Gaps & Grounding Plan

**Created:** 2026-06-13 (surfaced during the F-115 shipped-YAML self-sufficiency sweep)
**Status:** ⚠️ Preliminary — needs proper ingestion before the shipped YAML can be called fully grounded.

## Why this doc exists

The shipped KB entries `deliverables/ai/P2/architecture/boot-rom/taqoz-forth.yaml` and
`p2-monitor.yaml` currently rest **partly on preliminary web research**, not on a primary
source. The YAMLs are honest about this (they carry `knowledge_gaps` with explicit
`status:` notes), but the *research-direction breadcrumbs* (where to dig, which working
files to mine) do not belong in shipped YAML — they live here, in the ingestion tree.

This is a **content-confidence** concern, not a YAML correctness bug: the verified facts in
those entries (entry sequence from Silicon Doc v35 + P2 Datasheet, ROM residence) are
sound; the **interactive-Forth/Monitor capability detail** is what needs grounding.

## Current local material (this source folder)

- `taqoz-web-research-preliminary.md` — **direction-finding only, NOT a source for facts.**
- `taqoz-narrative.txt` — narrative summary.
- **Not yet here:** Peter Jakacki's `TAQOZ.spin2` source; an extraction of the ROM dictionary.

## Primary sources to ingest (the grounding plan)

1. **Parallax P2 boot ROM listing (`ROM_Booter.lst`, ~411 KB assembled ROM image)** — mine for:
   - the actual TAQOZ **word dictionary** (which words are in ROM vs. TAQOZ Reloaded only)
   - the **ROM Monitor command parser** (full command grammar; modify-command syntax)
2. **Peter Jakacki's `TAQOZ.spin2`** (linked from the forum threads; SourceForge/GitHub) —
   closest representation of the ROM build. Verify dictionary, extension mechanism
   (`BACKUP`/`RESTORE` word semantics), memory footprint.
3. **Forum threads (SME: Peter Jakacki, forums.parallax.com):**
   - "TAQOZ – Tachyon Forth for the P2 BOOT ROM" (design discussion, source links)
   - "Try these TAQOZ code snippets" (concrete usage examples)
4. **TAQOZ Reloaded 2.8 "Glossary of Words"** — comprehensive but Reloaded-superset; must
   be filtered to the ROM subset.

## Specific gaps (mirrored from the shipped YAMLs' `knowledge_gaps`)

**TAQOZ Forth** (`taqoz-forth.yaml`):
- word dictionary; runtime capabilities beyond "interactive REPL"; whether TAQOZ is
  invocable from running user code (vs. boot-window only); hub-RAM footprint when active;
  persistent user-word extension mechanism; ROM-vs-Reloaded word diff.

**ROM Monitor** (`p2-monitor.yaml`):
- full command grammar beyond the 2 Datasheet examples; modify-command syntax.

## Action

A proper `ingest-source` pass once `TAQOZ.spin2` and/or a `ROM_Booter.lst` extraction is
staged. Do **not** fabricate capability detail from the preliminary web research. When
grounded, fold results back into `taqoz-forth.yaml` / `p2-monitor.yaml` and close the
`knowledge_gaps` items.
