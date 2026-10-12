# p2kb-mcp 1.5.1 — `p2kb_obex_get` summary change request

**From:** the P2-Knowledge-Base YAML head (the KB).
**To:** the agent maintaining `P2-Knowledge-Base-MCP` (the `p2kb-mcp` server).
**Target release:** p2kb-mcp **1.5.1** (Stephen, 2026-10-11).
**Closes:** register finding **F-571** (`engineering/operations/P2KB-CORRECTION-FINDINGS.md`) when §6 passes.
**Scope:** `p2kb_obex_get` only. `p2kb_obex_find`, `p2kb_obex_download`, the delivery filter, the
index and every `p2kb_get` path are unchanged.

---

## 1. What is wrong today (measured on 1.5.0, 2026-10-11)

`p2kb_obex_get 2842` returns:

```json
"metadata": { "created_date": "", "file_size": "5883 B", "quality": 0, "version": "" }
```

- **`quality: 0`** on every object. The KB no longer carries `quality_score` (removed in KB v1.24.0:
  the KB does not rate OBEX objects). The server shows its zero value, which an agent reads as a
  rating of zero.
- **`created_date: ""`** on every object. The server reads `object_metadata.metadata.created_date`;
  in KB v1.24.0 that block was renamed `scrape_tracking` (scraper bookkeeping, removed by the delivery
  filter), so the path is empty.
- **`version: ""`** on every object where OBEX publishes no version — an empty string carries nothing.

The YAML tags compiled into the 1.5.0 binary show the summary is built from a fixed list:
`object_metadata` → `title`, `author`, `author_username`, `urls.*`, `technical_details.*`,
`functionality.*`, and `metadata` → `created_date`, `quality_score`, `discovery_date`,
`last_verified`, `extraction_status`. Any field outside that list never reaches an agent through this
tool, and any rename on our side silently empties a field on yours. That coupling is the real defect;
§3 removes it.

## 2. What the KB does (KB v1.24.1 — shipping before 1.5.1)

The upload date moves to the place the server already reads:

```yaml
object_metadata:
  ...
  metadata:
    created_date: '2022-01-04'     # the OBEX upload date, served (not bookkeeping)
  version_tracking:
    has_github_repo: false
```

- 129 of the 130 objects carry a date; one (2816) has none and has **no** `metadata:` block.
  (`_template.yaml`, the 131st file in the folder, is a template, not an object.)
- `version_tracking.obex_upload_date` no longer exists. The scraper writes `metadata.created_date`.
- `metadata` holds **only** `created_date`. `quality_score`, `discovery_date`, `last_verified` and
  `extraction_status` are not in any served object and will not return.

So on 1.5.0, after KB v1.24.1 and a refresh, `created_date` is already right. 1.5.1 is about §3.

## 3. The changes for 1.5.1

1. **Remove `quality`** from the `p2kb_obex_get` result, and the `quality_score` field from the
   struct. The KB does not rate OBEX objects and never will (KB doctrine, 2026-10-11: *an OBEX entry
   carries what the catalog says, never our verdict on it*).
2. **Omit an empty field instead of returning `""`.** In `metadata`: `created_date` absent or empty →
   leave the key out; same for `version` and `file_size`. If all three are empty, omit `metadata`.
   Sources, as today: `created_date` ← `object_metadata.metadata.created_date`; `file_size` ←
   `object_metadata.technical_details.file_size`; `version` ← `object_metadata.technical_details.version`.
3. **Drop the dead struct fields** `discovery_date`, `last_verified`, `extraction_status` and
   `quality_score` from whichever struct holds them (the binary shows their YAML tags beside
   `created_date`; no served object has any of them).
4. **Add `full_metadata`: the whole object, as delivered.** The `object_metadata` mapping of the
   object YAML **after the delivery filter** (the same filtered body `p2kb_get p2kbCommunity<id>`
   returns), parsed and emitted as a JSON object. This is the field our OBEX spec has always specified
   (`OBEX-IMPLEMENTATION-SPEC.md`, `ObexGetResult.full_metadata`). With it, a field the KB adds or
   renames reaches agents with no server change — the same move the delivery filter made when the
   rule started travelling with the content. The summary fields above stay for convenience; agents
   that need more read `full_metadata`.
   - **Filtering:** exactly the delivery filter you already apply to every KB body
     (`MCP-DELIVERY-FILTER-HANDOFF.md` §4, §5.1) — `remove_fields` at every depth (so
     `scrape_tracking` and any `source` key, e.g. `compatibility.source`, are gone) and column-0
     comments. Build `full_metadata` from the filtered body, never the raw one.
   - **Encoding:** the parsed YAML mapping emitted as JSON as-is — strings stay strings (dates are
     quoted in the YAML, so they arrive as strings), booleans and lists as parsed, key order not
     significant. No size cap: the largest object YAML is a few kilobytes.

5. **Categories come from the data, not the tool description.** `p2kb_obex_find`'s `category`
   parameter description hard-codes nine values ("drivers, misc, display, demos, audio, motors,
   communication, sensors, tools"). Those were our scraper's own buckets. From KB v1.24.2 every object
   carries **OBEX's own category** as the catalog page shows it (e.g. `Protocol`, `Display`,
   `Data Storage`, `Math`, `Sensor`, `Tool`), a string, or a list when OBEX lists several (F-573). So:
   - drop the enumerated list from the parameter description; say "an OBEX category — call with no
     parameters for the current list with counts";
   - build that no-parameter listing from the objects' `functionality.category` values (a list value
     counts once per category);
   - match `category` case-insensitively against the string, or any element of the list.
   The same KB release also mirrors `tags`, `languages`, `microcontroller`, `title` and `author` from
   the catalog and adds `technical_details.content_type` and `technical_details.licence` — no server
   change needed for those beyond what `full_metadata` (4) already carries.

Proceed on all five unless you object.

**Unchanged:** `object_id`, `title`, `author`, `category`, `description` (from
`functionality.description_short`, exactly as today), `download_url`, `download_instructions`, `languages`, `tags`,
`obex_page`, `metadata.file_size`; the multi-match `type: suggestions` response; search/browse output; caching (an object whose YAML changed has a new
`sha256`/`mtime` in the index and is re-fetched as today).

## 4. Result shape after 1.5.1

```json
{
  "object_id": "2842",
  "title": "Full Duplex Serial",
  "author": "Jon McPhalen (jonnymac)",
  "category": "communication",
  "description": "This object is a P2 update to FullDuplexSerial for the P1. ...",
  "download_url": "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842",
  "download_instructions": { "...": "unchanged" },
  "languages": ["SPIN2", "PASM2"],
  "tags": ["serial", "demo", "led", "driver", "spi"],
  "obex_page": "https://obex.parallax.com/obex/full-duplex-serial-2/",
  "metadata": { "created_date": "2022-01-04", "file_size": "5883 B" },
  "full_metadata": { "object_id": "2842", "title": "Full Duplex Serial", "...": "the whole filtered object_metadata" },
  "type": "obex_object"
}
```

## 5. Order

KB v1.24.1 publishes first (the date is in place). 1.5.1 can be built and unit-tested against it at
any time after; it does not depend on any other KB change.

## 6. Acceptance probes

**Precondition:** KB v1.24.1 is published (its tag on the remote), 1.5.1 is installed, and
`p2kb_refresh include_obex` has been run. Without v1.24.1, O2 fails for a reason that is not 1.5.1's.

| # | Probe | Expect |
|---|---|---|
| O1 | `p2kb_version` | `mcp_version 1.5.1`; `filter_rule_source: index` and `filter_engine_version: 1` as 1.5.0 reports them today |
| O2 | `p2kb_obex_get 2842` | `metadata` is exactly `{created_date: "2022-01-04", file_size: "5883 B"}` — no `quality` key anywhere, no `version` key (OBEX publishes none) |
| O3 | `p2kb_obex_get 2816` | no `metadata` key at all (2816 has no date, and its `file_size` and `version` are empty) |
| O4 | `p2kb_obex_get 2842` → `full_metadata` | present; contains `compatibility`, `version_tracking`, `metadata`; contains no `scrape_tracking` and no `source` key at any depth |
| O5 | `p2kb_obex_get "full duplex serial"` (a multi-match search) | as on 1.5.0: `type: suggestions`, a `suggestions` list of `{author, category, description, match_type, object_id, title}`; no `metadata` or `full_metadata` in suggestions |
| O6 | `p2kb_obex_find term:serial limit:2` | same shape as on 1.5.0: `{count: 2, objects: [{author, category, description, match_type, object_id, title}, …], term: "serial", type: "objects"}`; from KB v1.24.2 each `description` is the object's one-line description and `category` is OBEX's own (a list where the object has several) |
| O7 | `p2kb_obex_find` (no parameters), then `p2kb_obex_find category:"Protocol"` | the category list is OBEX's own names with counts, built from the objects (§3.5); the filter returns every object whose category is, or includes, Protocol |

F-571 closes in the register on O1-O7, with the server version.

## 7. Your review (2026-10-11) — our answers

1. **Breaking change — agreed.** `metadata.quality` goes and the other `metadata` keys appear only
   with a value; mark it breaking in the 1.5.1 changelog entry despite the patch number.
2. **Two version fields — `technical_details.version` is authoritative.** `version_tracking.obex_version`
   is a second copy the scraper writes from the same scrape; it equals `technical_details.version` in
   all 130 objects today (20 carry a value), and nothing reads it. The KB removes it in its next
   release so there is one field, not two. Read `technical_details.version` only, as §3.2 says.
3. **The shared spec — updated.** `engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`'s
   `p2kb_obex_get` row now states the 1.5.0 shape and the 1.5.1 contract (breaking, field sources,
   `full_metadata`). Re-import it byte-identical from the KB's `main`; `DOCs/API.md` and
   `docs-src/data/tools.yml` are yours as you said.
4. **2842's cut-off `description_short` ("andthe") — the KB's to fix, no server change.** Our scraper
   builds `description_short` as the first 100 characters of the description, cutting mid-word (50 of
   130 objects), and 2842's also lost a space. The KB corrects the field in its next release; keep
   reading `functionality.description_short` for `description` exactly as today.
