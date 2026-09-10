# TAQOZ Forth / ROM Monitor — Content Gaps & Grounding Plan

**Created:** 2026-06-13 (surfaced during the F-115 shipped-YAML self-sufficiency sweep)
**Status:** 🟡 **Partly grounded 2026-09-10** — the ROM listing has been mined; the Jakacki
half is still not runnable. See *Grounding progress* below before planning any work here.

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

## Grounding progress — 2026-09-10

**Mined the ROM listing. Two of the plan's four sources are now answered from the ROM itself.**

🔴 **First, a correction that changes what "the ROM listing" means.** This plan named
`ROM_Booter.lst`. That is the **FPGA** build (`ver = "A"`, *Prop123-A9 / BeMicro-A9*). The chip's
ROM is **`rom_booter_v33_01j.lst`** (`ver = "G"`, *Prop2 Silicon v2*) — same source v141,
different build target, ~3,300 lines apart. Mining the file this plan named would have described
a ROM that is not in the chip. Filed as **F-421**; all work below reads the silicon listing.

**Produced, in `sources/rom-booter/`:**

| Artifact | Answers |
|---|---|
| `taqoz-rom-dictionary.md` + `romdict-data.json` | *"the actual TAQOZ word dictionary"* — **432 words**, 50 immediate, with addresses and code targets, plus **17 words commented OUT** and therefore not in ROM. Self-checked: all 432 rebuilt names match the length the listing declares independently. |
| `rom-monitor-command-grammar.md` | *"the ROM Monitor command parser (full command grammar; modify-command syntax)"* — the complete 8-command dispatch, the `[xxxxxx]<cmd>` line format, case-insensitivity, and the digit-count rule that distinguishes cog/LUT from hub. **The modify command is `:`** (Download); there is no separate examine-and-alter syntax. |
| `rom-facility-map.md` | Stephen's question — *what facilities are in the ROM that we should be documenting* — as an address map of the 16 KB. |

**ROM TAQOZ is v33h** (`taqoz_name`, `$FD054`; `taqoz_version = 1_1`). That settles the shape of
the ROM-versus-Reloaded question: **Reloaded 2.8's glossary is a superset claim** against v33h and
must be filtered by the 432-word list, not merged with it.

**Still not runnable:** Jakacki's `TAQOZ.spin2` is still absent from the repo, so plan item 2
cannot proceed. It is now needed for *less* than before — the dictionary and Monitor grammar are
answered from the ROM — but the **word-level semantics** (what each of the 432 words does, and
their stack effects) are not, and that is what item 2 was really for.

**Deliberately not done:** the dictionary carries names, addresses, targets and the immediate
flag. It does **not** carry semantics or stack effects, because those live in the code at each
target address and this pass did not read them. Nothing about a word's behaviour may be inferred
from its name.

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
