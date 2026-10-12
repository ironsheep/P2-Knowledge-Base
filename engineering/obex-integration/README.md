# OBEX Integration — Status Dashboard

> The **OBEX head**'s front door. OBEX = the Parallax Object Exchange (community
> code objects). This head ingests OBEX objects + metadata into the KB so agents
> can discover and download community code via the p2kb MCP.
> _Linked from `engineering/README.md` (the heads board)._

## Tier 1 — At a glance
- **State:** ✅ **Integrated — a pure mirror** (KB **v1.24.4**, 2026-10-12). Each object holds only what its OBEX catalog page publishes: title, author, category, tags, description (its links keep their URLs), content type, microcontroller, languages, licence, upload date, page and download link. Beside those it has an **authored one-line description**, Stephen-approved and adversarially reviewed. Nothing of ours is carried: no classification, compatibility, version, size, scraper bookkeeping or placeholders. 5 objects have no download link because OBEX offers none.
- **Coverage:** **130 P2 objects**, which is every P2 object page on the OBEX listing on 2026-10-12. The KB's own capability-spine classification (domains A–K) is kept engineering-side in `obex-capability-map.yaml` and is not served.
  (E comms 25 · G displays 21 · F sensors 20 · B smart-pins 15 · C math/DSP 9 · H motors 9 · I storage 8 · K dev-tools 8 · A core 7 · J audio 7 · D streaming 1).
- **Served via:** the p2kb MCP — `p2kb_obex_find` / `p2kb_obex_get` / `p2kb_obex_download` (all 130; verified live 2026-10-12 on p2kb-mcp 1.5.0). p2kb-mcp 1.5.1 removes the summary's `quality: 0`, the fixed category list and the dead download links (`engineering/tools/p2kb-mcp/MCP-OBEX-SUMMARY-CHANGE-REQUEST.md`, F-571).
- **Last release:** **2026-10-12 (KB v1.24.4)** · **catalog mirrored 2026-10-12** · **new-object baseline = 2026-10-12**: the listing was re-scanned, and 130 object pages were listed, all already in the KB, with 0 new.
- **Why this head:** community code agents were never trained on, surfaced on-demand with authentic
  attribution + provenance — extends the KB beyond Parallax's own docs.

## Tier 2 — Outstanding work
| Item | State | Note |
|------|-------|------|
| **Pure mirror** | ✅ done 2026-10-12 (KB v1.24.2–v1.24.4) | every field from the page; 130 one-liners (F-573); non-catalog fields removed (Stephen: "pure mirror"), `capability` moved to `obex-capability-map.yaml` |
| **Re-scan for new objects** | ✅ 2026-10-12 | `discover`: 130 listed, 0 new; next re-scan uses the runbook below |
| **p2kb-mcp 1.5.1** | ⏳ server side | change request ready; F-571 closes on its probes O1-O7 |
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

**Run a delta re-scan** against the current baseline (**2026-10-12**). One tool does it all:
`engineering/tools/obex-integration/obex-catalog-mirror.py`, the **only** writer of the object YAMLs.
Its requests are polite: 2.5 s apart, with a neutral project User-Agent and never a personal address.
The 2025 scrapers are retired (`archive/`, local).
1. **New objects** — `discover --pages DIR` lists every P2 object page on the OBEX listing that has
   no YAML. For each one, run `add --url <page> --pages DIR`, which writes the id and page only.
   `NOT LISTED` lines are objects OBEX no longer lists; that is Stephen's call, so never delete one
   unasked.
2. **Catalog fields** — `fetch`, then `report` (read every change; a PROBLEM line is a page shape
   the tool does not know, so fix the tool, never force), then `apply`, which writes each object
   whole. Prove the run against git: every value outside the reported changes is unchanged.
3. **One-liners** — author `functionality.description_short` for each new or materially changed object
   from its catalog text (one sentence, ≤120 characters, no verdict), have a fresh agent check each
   against the full description; the release gate *OBEX One-Line Descriptions* fails until done.
4. **Capability map** — classify each new object in `obex-capability-map.yaml`. This is
   engineering-side, for the coverage analysis, and is never written into the object.
5. Release via `release-yamls`; probe live after the CDN window (`p2kb_refresh flush include_obex`).

### Close-out checklist — DO EVERY re-scan (this is what v2.2 missed) ⚠️
The YAML/index/release half rides `release-yamls`, but the **status docs do not update themselves** — a
re-scan is not done until ALL of these are refreshed in the **same** effort:
1. [ ] **This dashboard** — Tier 1 (state / coverage counts / last-release / **baseline date**) + the Tier 2 re-scan row.
2. [ ] **`OBEX-INTEGRATION-COMPLETE.md`** — append the vN.N delta section (counts, new/changed IDs, validation).
3. [ ] **Reset the delta baseline** to the new scrape date — in *both* this dashboard AND `whats-next` SKILL.md
   (the obex row in the head table + §"choose a target" obex line) so `whats-next` resumes from the right baseline.
4. [ ] **Memory pointer** `project_release_and_obex_dashboard_panels` — update the baseline date.
5. [ ] **Confirm the release** — index regenerated + `release-yamls` ran + the objects are in the tagged KB release + MCP re-served (content-probe a new ID).
6. [ ] **One-liners** — every new object has its authored `description_short` (the release gate enforces it).

> **Why a checklist here and not a skill:** OBEX is the one multi-artifact head without a working skill
> (ingestion has `ingest-source`, manual has `prepare-/release-manual`, yaml has
> `yaml-knowledge-base-maintenance`). Until/unless an `obex-rescan` skill exists, this checklist is the
> single home for the re-scan's definition-of-done. v2.2 (2026-06-29) did the data + release but left this
> dashboard, the baseline, and the memory pointer stale for ~5 days — exactly the gap this list closes.
