# OBEX Integration — Status Dashboard

> The **OBEX head**'s front door. OBEX = the Parallax Object Exchange (community
> code objects). This head ingests OBEX objects + metadata into the KB so agents
> can discover and download community code via the p2kb MCP.
> _Linked from `engineering/README.md` (the heads board)._

## Tier 1 — At a glance
- **State:** ✅ **Integrated** — **v2.2 Delta Re-Scrape (2026-06-29)**, released in **KB v1.13.3 (2026-07-03)**. Production-ready. (v2.1 base was 2025-09-12.)
- **Coverage:** **130 P2 objects** (100% P2-specific; P1 filtered out), all capability-spine classified across domains A–K
  (E comms 25 · G displays 21 · F sensors 20 · B smart-pins 15 · C math/DSP 9 · H motors 9 · I storage 8 · K dev-tools 8 · A core 7 · J audio 7 · D streaming 1).
  v2.2 added **17 new / 3 changed** vs the v2.1 (113-object) baseline.
- **Served via:** the p2kb MCP — `p2kb_obex_find` / `p2kb_obex_get` / `p2kb_obex_download` (index regenerated in v1.13.3; all 130 present).
- **Last release:** **2026-07-03 (KB v1.13.3)** · **delta baseline for the next re-scan = 2026-06-29** (the v2.2 scrape date).
- **Why this head:** community code agents were never trained on, surfaced on-demand with authentic
  attribution + provenance — extends the KB beyond Parallax's own docs.

## Tier 2 — Outstanding work
| Item | State | Note |
|------|-------|------|
| **Re-scan for delta** | ✅ done 2026-06-29 (v2.2) | 130 objects (17 new / 3 changed) in KB v1.13.3; next baseline **2026-06-29** |
| OBEX adoption outreach | ⏳ community-side | 6 archiver imports await author adoption → `OBEX-ADOPTION-REQUESTS.md` |
| Forum announcement follow-through | ◐ | drafts `FORUM-POST-1/2` (KB announcement + integration) |

## Tier 3 — Drill-down
- **Integration record** → `OBEX-INTEGRATION-COMPLETE.md` (the 2025-09-12 completion report + metrics)
- **Plan / methodology** → `OBEX-INTEGRATION-PLAN.md` · `OBEX-EXECUTION-PLAN-FOR-SONNET.md`
- **Adoption requests** → `OBEX-ADOPTION-REQUESTS.md`
- **Community comms** → `FORUM-POST-1-P2-KB-ANNOUNCEMENT.md` · `FORUM-POST-2-OBEX-INTEGRATION.md`
- **Scan/scrape tooling** → `engineering/tools/obex-integration/`
- **Dashboard panel** → the OBEX last-release panel is also surfaced on the manual/release dashboards.

## Re-scan runbook (the OBEX head has no dedicated skill — this IS the runbook)

**Run a delta re-scan** against the current baseline (**2026-06-29**): pull the live OBEX object set
(`obex_discovery_fixed.py` listing crawl + per-object structured extraction), diff against the served
YAMLs, ingest new/changed objects (same metadata-extraction + capability-spine + QA pipeline), regen the
index, and release via `release-yamls`.

### Close-out checklist — DO EVERY re-scan (this is what v2.2 missed) ⚠️
The YAML/index/release half rides `release-yamls`, but the **status docs do not update themselves** — a
re-scan is not done until ALL of these are refreshed in the **same** effort:
1. [ ] **This dashboard** — Tier 1 (state / coverage counts / last-release / **baseline date**) + the Tier 2 re-scan row.
2. [ ] **`OBEX-INTEGRATION-COMPLETE.md`** — append the vN.N delta section (counts, new/changed IDs, validation).
3. [ ] **Reset the delta baseline** to the new scrape date — in *both* this dashboard AND `whats-next` SKILL.md
   (the obex row in the head table + §"choose a target" obex line) so `whats-next` resumes from the right baseline.
4. [ ] **Memory pointer** `project_release_and_obex_dashboard_panels` — update the baseline date.
5. [ ] **Confirm the release** — index regenerated + `release-yamls` ran + the objects are in the tagged KB release + MCP re-served (content-probe a new ID).

> **Why a checklist here and not a skill:** OBEX is the one multi-artifact head without a working skill
> (ingestion has `ingest-source`, manual has `prepare-/release-manual`, yaml has
> `yaml-knowledge-base-maintenance`). Until/unless an `obex-rescan` skill exists, this checklist is the
> single home for the re-scan's definition-of-done. v2.2 (2026-06-29) did the data + release but left this
> dashboard, the baseline, and the memory pointer stale for ~5 days — exactly the gap this list closes.
