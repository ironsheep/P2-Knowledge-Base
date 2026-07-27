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
| **YAML (P2KB)** | [dashboard](operations/YAML-HEAD-DASHBOARD.md) · [register](operations/P2KB-CORRECTION-FINDINGS.md) | **v1.14.1** shipped · no open corrections (F-183 ingestion-tracked) | Next correction/enrichment as findings land |
| **Manual** | [`document-production/README.md`](document-production/README.md) · [roster](document-production/PUBLICATION-ROSTER.md) | 8 live manuals + **7 app-notes** · **Getting Started v1.0.2 · Architect's Guide v1.0.2 · Streamer Guide v1.0.7 released 2026-07-21** (readability/voice pass — closing-cadence + register tics evened, no technical change) · **Interpreters & Emulators (XBYTE) v1.0.0 released 2026-07-20** (initial community-review release — the XBYTE hardware bytecode engine → custom VM + illustrative CPU emulator; Chip-reviewed, review-delta changeset-audited) · **I/O & Smart Pins v1.0.7 released 2026-07-16** (Ch.9 §9.1 complementary-output/dead-band note — two coordinated Smart Pins, not one; twin of KB v1.14.5, F-225) · **Assembly v3.1.4 released 2026-07-14** (F-214 render-only patch — hyphenated names print as authored; the cross-ref to the I/O & Smart Pins guide now names a manual that exists; zero content change) · **Debug Window v1.1.1 released 2026-07-27** (run-verification patch — all 34 examples run on PNut v55 silicon; F-227 the `PC_KEY`/`PC_MOUSE` escape backtick the manual itself taught wrong, F-228 a keyword-named display never opens + the definitive 103-word naming rule from the PNut source) · **P2AN007 v1.0.0** (2026-07-13, STRUCT + cross-cog data sharing; EF-036..EF-040) · fleet correction wave 2026-07-12 re-released 11 docs (I/O & Smart Pins v1.0.5, DeSilva v3.0.3, Streamer v1.0.6, Architect v1.0.1, Getting Started v1.0.1, P2AN001 v1.0.2, P2AN002-006 v1.0.x) · Single-Step in review · **F-215 deferred** (app-note Revision History — 6 of 7 app notes; rides each doc's next natural release) | Single-Step Debugger |
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
