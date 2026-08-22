# Engineering — Heads Board (front door)

> The **operational map** of the P2-Knowledge-Base engineering effort: the *heads*
> (independent work-fronts under one repo), each head's status at a glance, and
> **the next actionable thing in each**. Per-head detail lives in that head's own
> dashboard — this board links out, it does not duplicate.
>
> **This is the static map. `whats-next` is the guided entry.** Run the
> `whats-next` skill at session start — it reads the `active_element` pointer,
> resumes your thread, and routes you into the right head. This README is what you
> read to see the *whole board* and decide where to push next.
>
> _Last refreshed: 2026-07-05._

## The heads — status & next action

Glance only — one line per head; each head's own dashboard (Dashboard column) holds the detail.

| Head | Dashboard | Status at a glance | Next actionable |
|------|-----------|--------------------|-----------------|
| **Ingestion** | [`ingestion/README.md`](ingestion/README.md) | 32 sources · 8 open gaps + 3 expert-Qs | Smart Pins manual cert audit → 5B verification fill |
| **YAML (P2KB)** | [dashboard](operations/YAML-HEAD-DASHBOARD.md) · [register](operations/P2KB-CORRECTION-FINDINGS.md) | **v1.16.0** shipped 2026-08-08 (Spin2 preprocessor corrections F-229…F-233 + ENH-02/03/04, compiler-verified on PNut-TS v1.55.2; licensing statements removed KB-wide) | Next correction/enrichment as findings land |
| **Manual** | [`document-production/README.md`](document-production/README.md) · [roster](document-production/PUBLICATION-ROSTER.md) | 8 live manuals + **7 app-notes** · **ALL 15 re-released 2026-08-08 — the CC BY-SA 4.0 licensing wave** (Assembly v3.1.5 · I/O & Smart Pins v1.0.8 · Debug Window v1.1.2 · DeSilva v3.0.4 · XBYTE v1.0.1 · Streamer v1.0.8 · Architect v1.0.3 · Getting Started v1.0.3 · P2AN001 v1.0.3 · P2AN002-005 v1.0.2 · P2AN006/007 v1.0.1). BY-NC-ND reverted to CC BY-SA 4.0 across every document; **zero technical content changed**. Each PDF verified against three independent expectations (an interactive-daemon build of the same source, the prior published PDF, and the compile log's own page count) — all 15 page counts match their logs exactly, no content drop. Two page-count moves investigated rather than accepted: **Assembly 505→503** and **DeSilva 164→162**, both the same tighter table packing (DeSilva's prior build had two pages holding only ~400-650 chars where a table was pushed whole onto a fresh page) · **F-215 deferred** (app-note Revision History — rides each doc's next natural release) · **DeSilva v3.0.5 released 2026-08-11** (164pp) — reader-reported, bench-verified worked-example correctness (smart-pin `P_OE`, reserved-word serial examples, quadrature B-phase routing) + per-board LED pin guidance · **THREE RELEASED 2026-08-17** — DeSilva **v3.0.6** (166pp; an honest platform comparison, and Ch.16 on DIR/OUT being OR'd across cogs so two drivers produce a result resembling neither), P2AN001 **v1.0.4** (I/O power domains are groups of FOUR, not eight — the Edge's eight-pin grouping is the LDO/header layer), P2AN002 **v1.0.3** (Recipe 6 keeps hub access out of both CORDIC loops; the released v1.0.2 shape loses results SILENTLY on real silicon). Debug Window **v1.1.3 released 2026-08-18** (168pp; the omitted-FFT-argument chapter, plus four repairs that had shipped — a literal `^{}` from a pre-escaped caret, an inverted code-span cascade, and two identifiers running into the margin; first release verified by measuring margin overflow rather than by eye). I/O & Smart Pins **v1.0.9 released 2026-08-18** (396pp; USB bus power told correctly, and every worked-example code line brought inside its box — F-289's real scope was 11 lines, not the 2 on record, one of them already past the box border in released v1.0.8). Assembly **v3.1.6 released 2026-08-18** (502pp; hub access kept out of both CORDIC loops, plus three repairs that had shipped — 16 syntax lines printing a literal `&nbsp;`, two identifiers in the margin, and an Appendix G constant table that printed its names ON TOP of their bit patterns, fixed at the platform by sizing those columns to content). XBYTE **v1.1.0 released 2026-08-19** (114pp, was 100; the structural restructure from community review — seven Parts ordered by the reader's decision with a new Part III "Choosing Your Rung" ahead of the engine, a second worked build between the smallest program and the 6502, three new figures, and the column-map notation for shared handler bodies taught and adopted in the shipped corpus. §7.4 no longer reads as a wall: the engine relocates per-instruction work rather than forbidding it, and where the work goes is a before/after-the-work timing decision — nine downstream sites that still said "nowhere to put the work" were swept). Streamer **v1.0.9 released 2026-08-19** (76pp, was 73; Goertzel rewritten as a buildable detector grounded line-by-line in the Parallax documentation's own worked program, a new §14.5 on `-d` putting the highest-priority interrupt in the streaming cog, and §9.2 rewritten end to end — the released v1.0.8 wrote a pin number into a command field that does not exist in that mode, which silently selected a different mode. Three margin overruns were found by measuring the rendered PDF and fixed before the build; one of them was a regression from this release's own bolding pass, and the compile log was clean before and after all three) · **Streamer v1.1.0 released 2026-08-22** (91pp, was 76 — the DAC-pin procedure every routing example depended on and never had, the LUT window's eight loop sizes, and streamer pin behaviour sealed on silicon (EF-062). **First document to carry machine-readable copyright and licence (F-316)**, and the first to prove metadata single-sourcing on a returned PDF: v1.0.9 shipped with Title, Subject and Author all EMPTY. Both are now gated by `audit-pdf-metadata.py`. Rides KB v1.17.0.) | Single-Step Debugger + PNut-Term-TS Guide (co-release; the tool has now shipped) |
| **OBEX** | [`obex-integration/README.md`](obex-integration/README.md) | ✅ v2.1 (2025-09-12) · 113 P2 objects · MCP-served | Delta re-scan vs the 2025-09-12 baseline |
| **Operations** | [`operations/README.md`](operations/README.md) | Cross-cutting process · owns register + lessons-learned | (infrastructure — supports the content heads) |
| **Quick Bytes** | [`quickbytes-integration/README.md`](quickbytes-integration/README.md) | 🔴 NOT processed · ~15% discovered | Parked — not moving soon (tracked so it isn't lost) |

## How the heads work (the model)
- **~70% of work is single-head run-to-completion; ~30% interleaved** — progress a head, set it aside,
  pick another, sometimes return. The only state we actively store is one pointer: the todo-mcp context
  key `active_element` (`head:element`). Everything else is reconstructed from these dashboards + git.
- **Each head has a working skill** (its execution counterpart): ingestion → `ingest-source`;
  manual → `prepare-manual` / `release-manual`; yaml → `yaml-knowledge-base-maintenance`;
  obex/quickbytes → their integration pipelines.
- **Trust chain (sacred):** Trusted Sources → Trusted YAML → Trusted Documentation → Community.
  Every head preserves fidelity along this chain.

## Cross-cutting references
- **Process map** → [`operations/PROCESS-GUIDANCE-ARCHITECTURE.md`](operations/PROCESS-GUIDANCE-ARCHITECTURE.md)
- **Why the rules exist** → [`operations/lessons-learned/INDEX.md`](operations/lessons-learned/INDEX.md)
- **Repo structure** → [`STRUCTURE-GUIDE.md`](STRUCTURE-GUIDE.md) · [`ABOUT.md`](ABOUT.md)
- **Standards / procedures** → [`standards/`](standards/) · [`procedures/`](procedures/)
- **Public landing page** (project intent + content availability) → the repo-root `README.md`
  *(separate concern — the GitHub-facing pitch, not this operational board)*

---
*This board is the operational front door. Keep each row's "status / next" honest and current — a stale
board is worse than none. Detail belongs in the per-head dashboards; this stays glanceable.*
