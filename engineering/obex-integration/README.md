# OBEX Integration — Status Dashboard

> The **OBEX head**'s front door. OBEX = the Parallax Object Exchange (community
> code objects). This head ingests OBEX objects + metadata into the KB so agents
> can discover and download community code via the p2kb MCP.
> _Linked from `engineering/README.md` (the heads board)._

## Tier 1 — At a glance
- **State:** ✅ **Integrated** — v2.1 OBEX Community Release (2025-09-12). Production-ready.
- **Coverage:** **113 P2 objects** (100% P2-specific; P1 filtered out) · 24 unique authors · 9 categories
  (drivers 49 · misc 34 · display 7 · demos 5 · audio 5 · motors 5 · communication 4 · sensors 3 · tools 1).
- **Served via:** the p2kb MCP — `p2kb_obex_find` / `p2kb_obex_get` / `p2kb_obex_download`.
- **Last release:** **2025-09-12** — this is the **delta baseline** for the next re-scan.
- **Why this head:** community code agents were never trained on, surfaced on-demand with authentic
  attribution + provenance — extends the KB beyond Parallax's own docs.

## Tier 2 — Outstanding work
| Item | State | Note |
|------|-------|------|
| **Re-scan for delta** | ⏳ **outstanding** | No re-scan since the 2025-09-12 baseline. New / updated OBEX objects since then are unindexed. This is the head's primary next action. |
| OBEX adoption outreach | ⏳ community-side | `OBEX-ADOPTION-REQUESTS.md` — 6 GitHub-archiver imports await adoption by their original authors (ersmith, mike calyer, Riley August, …). Outreach, not KB work. |
| Forum announcement follow-through | ◐ | `FORUM-POST-1/2` drafted (KB announcement + integration). |

## Tier 3 — Drill-down
- **Integration record** → `OBEX-INTEGRATION-COMPLETE.md` (the 2025-09-12 completion report + metrics)
- **Plan / methodology** → `OBEX-INTEGRATION-PLAN.md` · `OBEX-EXECUTION-PLAN-FOR-SONNET.md`
- **Adoption requests** → `OBEX-ADOPTION-REQUESTS.md`
- **Community comms** → `FORUM-POST-1-P2-KB-ANNOUNCEMENT.md` · `FORUM-POST-2-OBEX-INTEGRATION.md`
- **Scan/scrape tooling** → `engineering/tools/obex-integration/`
- **Dashboard panel** → the OBEX last-release panel is also surfaced on the manual/release dashboards.

## Next action
**Run a delta re-scan** against the 2025-09-12 baseline: pull the current OBEX object set, diff against
the 113 indexed, ingest new/changed objects (same metadata-extraction + QA pipeline), and re-release.
