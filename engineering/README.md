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
| **Manual** | [`document-production/README.md`](document-production/README.md) · [roster](document-production/PUBLICATION-ROSTER.md) | 8 live manuals + **7 app-notes** · **ALL 15 re-released 2026-08-08 — the CC BY-SA 4.0 licensing wave** (Assembly v3.1.5 · I/O & Smart Pins v1.0.8 · Debug Window v1.1.2 · DeSilva v3.0.4 · XBYTE v1.0.1 · Streamer v1.0.8 · Architect v1.0.3 · Getting Started v1.0.3 · P2AN001 v1.0.3 · P2AN002-005 v1.0.2 · P2AN006/007 v1.0.1). BY-NC-ND reverted to CC BY-SA 4.0 across every document; **zero technical content changed**. Each PDF verified against three independent expectations (an interactive-daemon build of the same source, the prior published PDF, and the compile log's own page count) — all 15 page counts match their logs exactly, no content drop. Two page-count moves investigated rather than accepted: **Assembly 505→503** and **DeSilva 164→162**, both the same tighter table packing (DeSilva's prior build had two pages holding only ~400-650 chars where a table was pushed whole onto a fresh page) · **F-215 deferred** (app-note Revision History — rides each doc's next natural release) · **DeSilva v3.0.5 released 2026-08-11** (164pp) — reader-reported, bench-verified worked-example correctness (smart-pin `P_OE`, reserved-word serial examples, quadrature B-phase routing) + per-board LED pin guidance · **THREE RELEASED 2026-08-17** — DeSilva **v3.0.6** (166pp; an honest platform comparison, and Ch.16 on DIR/OUT being OR'd across cogs so two drivers produce a result resembling neither), P2AN001 **v1.0.4** (I/O power domains are groups of FOUR, not eight — the Edge's eight-pin grouping is the LDO/header layer), P2AN002 **v1.0.3** (Recipe 6 keeps hub access out of both CORDIC loops; the released v1.0.2 shape loses results SILENTLY on real silicon). Debug Window **v1.1.3 released 2026-08-18** (168pp; the omitted-FFT-argument chapter, plus four repairs that had shipped — a literal `^{}` from a pre-escaped caret, an inverted code-span cascade, and two identifiers running into the margin; first release verified by measuring margin overflow rather than by eye). Assembly **v3.1.6** and I/O & Smart Pins **v1.0.9** re-rendering | Single-Step Debugger + PNut-Term-TS Guide (co-release; the tool has now shipped) |
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
