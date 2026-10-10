# Quick Bytes Integration — Status Dashboard

> The **Quick Bytes head**'s front door. Quick Bytes = the Parallax "Quick Bytes"
> community code/tutorial series (object packages, with correlated video content).
> This head would ingest that series into the KB the way OBEX objects are.
> _Linked from `engineering/README.md` (the heads board)._

## Tier 1 — At a glance
- **State:** 🔴 **NOT PROCESSED** — long-standing outstanding work. Scaffolding exists; the
  integration has **never been executed**. **Parked at the bottom of the queue** — not moving soon
  (tracked so it isn't forgotten, not because it's imminent).
- **What exists vs. what's missing:**
  - ✅ **Plans staged** — `ingestion/plans/QUICK-BYTES-READY-TO-EXECUTE.md` + `quick-bytes-ingestion-plan.md` + summary.
  - ✅ **Scraper tooling staged** — `engineering/tools/quick-bytes-integration/scrape-quick-bytes.py` (+ tag-taxonomy / youtube-playlist-correlator tools referenced in the plan).
  - ◐ **Partial discovery** — `ingestion/sources/quick-bytes-code/` holds a few discovered objects (~15%) + `quick-bytes-discovery-manifest.md`.
  - 🔴 **This integration head (`engineering/quickbytes-integration/`) is otherwise empty** — no ingested catalog, no metadata extraction, no MCP serving.

## Tier 2 — Outstanding work (when it's eventually picked up)
| Item | State | Note |
|------|-------|------|
| Confirm intent / re-validate plan | ⏳ | The "ready to execute" plan carries a stale "next 2–3 days" note — re-confirm scope before running. |
| Run the scraper + discovery sweep | ⏳ | Complete the object/video correlation beyond the ~15% partial. |
| Metadata extraction + QA | ⏳ | Mirror the OBEX pipeline (authors, dates, categories, provenance). |
| Index + MCP serving | ⏳ | So agents can discover Quick Bytes objects like OBEX. |

## Source root (2026-10-10)
Parallax moved `www.parallax.com` to Shopify. **Every Quick Bytes article now lives under the OBEX docs
site:** `https://obex.parallax.com/docs/quick-bytes/propeller-2/<slug>/` (e.g. `.../starting-your-p2-project-with-a-spin2-template/`).
The 42 catalog entries in `deliverables/ai/P2/community/quick-bytes/` were re-rooted to it (twelve slugs also
changed; the entry filenames are the OLD slugs and stay, being KB keys). Code downloads there are plain
`/qbi/downloads/<file>` links on `obex.parallax.com`, not the old Parallax download manager. The scraper's
article root is updated; its link extractors (written for the old markup) and the tag-taxonomy index URL
in `extract-tag-taxonomy.py` still describe the old site and need re-pointing when the head is revived.

## Tier 3 — Drill-down
- **Execution plan** → `engineering/ingestion/plans/QUICK-BYTES-READY-TO-EXECUTE.md`
- **Plan + summary** → `engineering/ingestion/plans/quick-bytes-ingestion-plan.md` · `quick-bytes-ingestion-summary.md`
- **Discovery manifest** → `engineering/ingestion/sources/quick-bytes-discovery-manifest.md`
- **Partial source** → `engineering/ingestion/sources/quick-bytes-code/`
- **Tooling** → `engineering/tools/quick-bytes-integration/`

## Next action
**None scheduled** — deliberately parked. When revived: re-confirm the plan, then run the staged
scraper → discovery → metadata/QA → index pipeline (model it on the completed OBEX integration).
