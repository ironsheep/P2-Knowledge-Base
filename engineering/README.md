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
> _Last refreshed: 2026-06-24._

## The heads — status & next action

| Head | Dashboard | Status at a glance | Next actionable |
|------|-----------|--------------------|-----------------|
| **Ingestion** | [`ingestion/README.md`](ingestion/README.md) | 32 logical sources · 8 open gaps + 3 expert-Qs · **Smart Pins (Titus) rev5 ✅ today** | **Smart Pins manual cert audit** (uses Titus); then **5B verification fill** (~20 sources missing cross-source, image debt) |
| **YAML (P2KB)** | [`operations/YAML-HEAD-DASHBOARD.md`](operations/YAML-HEAD-DASHBOARD.md) · register → [`P2KB-CORRECTION-FINDINGS.md`](operations/P2KB-CORRECTION-FINDINGS.md) · data → `deliverables/ai/P2/` | **v1.11.0 in prep** — eval-header board model (10 boards standardized + HyperRAM authored + orphans removed) + F-161/F-160/F-162 · drains the Assembly-manual YAML gate · **open:** G-004/G-005 (Chip/HW-gated) | **Regenerate index + validate + release v1.11.0** |
| **Manual** | [`document-production/README.md`](document-production/README.md) · roster → [`PUBLICATION-ROSTER.md`](document-production/PUBLICATION-ROSTER.md) | Getting-Started **v1.0.0** ✅ + Assembly **v3.1.1** ✅ + DeSilva **v3.0.1** ✅ + Debug-Window **v1.0.1** ✅ + Streamer **v1.0.4** ✅ + **I/O & Smart Pins v1.0.1 ✅ shipped 2026-07-04** · Single-Step in **tech review** | **I/O & Smart Pins User Guide v1.0.1** — hardware-verified patch (Ch.5 event-wait timeout F-193 + Ch.15 A+B routing F-192); maiden v1.0.0 2026-07-03; cross-ref filter pilot. Next owned work: Architect's Guide + XBYTE guide; P2AN app-note series — **P2AN001 v1.0.1 + P2AN002 v1.0.0 + P2AN003 v1.0.0 + P2AN004 v1.0.0 ✅ released 2026-07-03** (ADC + CORDIC + DAC + freq/period/pulse; companion-schema pilot; P2AN004 adds rendered circuit/timing diagrams) |
| **OBEX** | [`obex-integration/README.md`](obex-integration/README.md) | ✅ Integrated v2.1 (2025-09-12) · 113 P2 objects · served via p2kb MCP | **Delta re-scan** vs the 2025-09-12 baseline |
| **Operations** | [`operations/README.md`](operations/README.md) | Cross-cutting process + dashboard home; owns the corrections register & lessons-learned | (infrastructure — supports the content heads) |
| **Quick Bytes** | [`quickbytes-integration/README.md`](quickbytes-integration/README.md) | 🔴 **NOT processed** — plans + scraper staged, ~15% discovered, never executed | **Parked at the bottom** — not moving soon (tracked so it isn't lost) |

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
