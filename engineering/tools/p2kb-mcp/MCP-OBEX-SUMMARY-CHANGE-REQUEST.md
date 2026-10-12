# p2kb-mcp 1.5.1 — `p2kb_obex_get` summary change request

**From:** the P2-Knowledge-Base YAML head (the KB).
**To:** the agent maintaining `P2-Knowledge-Base-MCP` (the `p2kb-mcp` server).
**Target release:** p2kb-mcp **1.5.1** (Stephen, 2026-10-11).
**Closes:** register finding **F-571** (`engineering/operations/P2KB-CORRECTION-FINDINGS.md`) when §6 passes.
**Scope:** `p2kb_obex_get`, plus `p2kb_obex_find`'s category list (§3.5) and an object with no
download (§3.6, which also touches `p2kb_obex_download`). The delivery filter, the index and every
`p2kb_get` path are unchanged.

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

## 2. What the KB has done (KB v1.24.1 and v1.24.2 — both published 2026-10-11/12)

**v1.24.1** moved the upload date to the place the server already reads:

```yaml
object_metadata:
  ...
  metadata:
    created_date: '2022-01-04'     # the OBEX upload date, served (not bookkeeping)
  version_tracking:
    has_github_repo: false
```

- From v1.24.2 all 130 objects carry a date (2816's came back with the catalog mirror).
  (`_template.yaml`, the 131st file in the folder, is a template, not an object.)
- `version_tracking.obex_upload_date` no longer exists. The scraper writes `metadata.created_date`.
- `metadata` holds **only** `created_date`. `quality_score`, `discovery_date`, `last_verified` and
  `extraction_status` are not in any served object and will not return.

So on 1.5.0, after KB v1.24.1 and a refresh, `created_date` is already right.

**v1.24.2** makes every OBEX object a mirror of its OBEX catalog page (F-573), with no server change
needed for any of it:
- `title`, `author`, `functionality.description_full`, `functionality.tags`,
  `technical_details.languages`, `technical_details.microcontroller` and `metadata.created_date` carry
  OBEX's own values; `technical_details.content_type` (`Code`, `Hardware`, `Tip`) and
  `technical_details.licence` (`MIT`, `Other`) are new.
- `functionality.category` is **OBEX's own category** — a string, or a **list** for the 32 objects
  OBEX files under several (§3.5).
- `functionality.description_short` — the field you serve as `description` — is now an authored
  one-sentence summary (≤120 characters) for every object, never a cut of the catalog text. Keep
  reading it exactly as today.
- `version_tracking.obex_version` is gone.

**v1.24.4** makes each object a **pure mirror** (Stephen, 2026-10-12): it holds the catalog's fields
and nothing of ours. Every object now has exactly this shape:

```yaml
object_metadata:
  object_id: '2842'
  title: Full Duplex Serial
  author: Jon McPhalen
  functionality:
    category: Protocol              # a string, or a list where OBEX lists several
    tags: []
    description_short: P2 update to FullDuplexSerial for the P1, with ...   # authored one-liner
    description_full: This object is a P2 update to FullDuplexSerial ...    # links keep their URL
  technical_details:
    content_type: [Code]
    microcontroller: [P2]
    languages: [PASM2, SPIN2]
    licence: Other
  metadata:
    created_date: '2022-01-04'
  urls:
    obex_page: https://obex.parallax.com/obex/full-duplex-serial-2/
    download_direct: https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842
```

- **Gone from every object:** `author_username`; `technical_details.version`, `file_size`,
  `file_format`; `urls.github_repo`, `documentation`, `forum_discussion`; `functionality.subcategory`,
  `hardware_support`, `peripherals`; and the whole `compatibility`, `version_tracking`, `capability`
  and `scrape_tracking` blocks.
  - `version` was a scraper's guess from the description text, and on three objects it was a tool's
    version, not the object's.
  - `github_repo` was also taken from the description. The description now keeps every link's URL
    after its words, so the repository link reaches the reader as OBEX shows it.
- **`urls.download_direct` is absent on 5 objects** (4442, 4571, 4581, 4616, 4617). OBEX offers no
  download for them: the page says "There are no downloads available for this object", and the ZIP
  link answers `invalid!`. Their descriptions point to GitHub instead (§3.6).

1.5.1 is about §3.

## 3. The changes for 1.5.1

1. **Remove `quality`** from the `p2kb_obex_get` result, and the `quality_score` field from the
   struct. The KB does not rate OBEX objects and never will (KB doctrine, 2026-10-11: *an OBEX entry
   carries what the catalog says, never our verdict on it*).
2. **Omit an empty field instead of returning `""`.** `metadata` is `{created_date}` from
   `object_metadata.metadata.created_date`; when that is absent or empty, omit `metadata`. **Drop
   `version` and `file_size` from `metadata`**: from KB v1.24.4 no object has either field (§2).
   OBEX publishes no size and no version field, and the old values were scraper guesses.
3. **Drop the dead struct fields**: `discovery_date`, `last_verified`, `extraction_status` and
   `quality_score` (the binary shows their YAML tags beside `created_date`), plus every field §2
   lists as gone (`author_username`, `version`, `file_size`, `file_format`, `github_repo`,
   `documentation`, `forum_discussion`, `subcategory`, `hardware_support`, `peripherals`). No
   served object has any of them.
4. **Add `full_metadata`: the whole object, as delivered.** The `object_metadata` mapping of the
   object YAML **after the delivery filter** (the same filtered body `p2kb_get p2kbCommunity<id>`
   returns), parsed and emitted as a JSON object. This is the field our OBEX spec has always specified
   (`OBEX-IMPLEMENTATION-SPEC.md`, `ObexGetResult.full_metadata`). With it, a field the KB adds or
   renames reaches agents with no server change — the same move the delivery filter made when the
   rule started travelling with the content. The summary fields above stay for convenience; agents
   that need more read `full_metadata`.
   - **Filtering:** exactly the delivery filter you already apply to every KB body
     (`MCP-DELIVERY-FILTER-HANDOFF.md` §4, §5.1) — `remove_fields` at every depth (so
     any `source` or `scrape_tracking` key is gone; from KB v1.24.4 an OBEX object has neither) and column-0
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

6. **An object with no download has no download URL.** Take `download_url` from
   `object_metadata.urls.download_direct`, never build it from the object id. When the key is absent
   (5 objects, §2):
   - `p2kb_obex_get` leaves out `download_url` and `download_instructions`;
   - `p2kb_obex_download` fetches nothing and says so: *"OBEX offers no download for object <id>;
     see its page <obex_page> — the description says where the code is."*

   Building the URL from the id gives these objects a link that answers `invalid!`, which an agent
   would read as a broken server or a corrupt ZIP.

Proceed on all six unless you object.

**Unchanged:** `object_id`, `title`, `author`, `category`, `description` (from
`functionality.description_short`, exactly as today), `download_url` and `download_instructions`
where the object has a download, `languages`, `tags`, `obex_page`; the multi-match `type: suggestions` response; search/browse output; caching (an object whose YAML changed has a new
`sha256`/`mtime` in the index and is re-fetched as today).

## 4. Result shape after 1.5.1

```json
{
  "object_id": "2842",
  "title": "Full Duplex Serial",
  "author": "Jon McPhalen",
  "category": "Protocol",
  "description": "P2 update to FullDuplexSerial for the P1, with numeric output changes and string formatting for complex output.",
  "download_url": "https://obex.parallax.com/wp-admin/admin-ajax.php?action=download_obex_zip&popcorn=salty&obuid=OB2842",
  "download_instructions": { "...": "unchanged" },
  "languages": ["PASM2", "SPIN2"],
  "tags": [],
  "obex_page": "https://obex.parallax.com/obex/full-duplex-serial-2/",
  "metadata": { "created_date": "2022-01-04" },
  "full_metadata": { "object_id": "2842", "title": "Full Duplex Serial", "...": "the whole filtered object_metadata" },
  "type": "obex_object"
}
```

## 5. Order

The KB side is complete from **v1.24.4** (2026-10-12). Build and test 1.5.1 against v1.24.4 or
later; it depends on no further KB change.

## 6. Acceptance probes

**Precondition:** KB v1.24.4 or later is published, 1.5.1 is installed, and
`p2kb_refresh flush:true include_obex:true` has been run at least 5 minutes after the last KB push
(GitHub raw's CDN holds files for 300 s; inside that window the server can fetch old bodies against
the new index and fail verification).

| # | Probe | Expect |
|---|---|---|
| O1 | `p2kb_version` | `mcp_version 1.5.1`; `filter_rule_source: index` and `filter_engine_version: 1` as 1.5.0 reports them today |
| O2 | `p2kb_obex_get 2842` | `metadata` is exactly `{created_date: "2022-01-04"}`; no `quality`, `version` or `file_size` key anywhere; `download_url` as in §4 |
| O3 | `p2kb_obex_get 4581`, then `p2kb_obex_download 4581` | the get has no `download_url` and no `download_instructions` (OBEX offers no download, §3.6); the download fetches nothing and returns the "no download" message naming the page |
| O4 | `p2kb_obex_get 2842` → `full_metadata` | present; its keys are exactly `object_id`, `title`, `author`, `functionality`, `technical_details`, `metadata`, `urls` (KB v1.24.4 shape, §2) |
| O5 | `p2kb_obex_get "full duplex serial"` (a multi-match search) | as on 1.5.0: `type: suggestions`, a `suggestions` list of `{author, category, description, match_type, object_id, title}`; no `metadata` or `full_metadata` in suggestions |
| O6 | `p2kb_obex_find term:serial limit:2` | same shape as on 1.5.0: `{count: 2, objects: [{author, category, description, match_type, object_id, title}, …], term: "serial", type: "objects"}`; from KB v1.24.2 each `description` is the object's one-line description and `category` is OBEX's own (a list where the object has several) |
| O7 | `p2kb_obex_find` (no parameters), then `p2kb_obex_find category:"Protocol"` | the category list is OBEX's own names with counts, built from the objects (§3.5); the filter returns every object whose category is, or includes, Protocol |

F-571 closes in the register on O1-O7, with the server version.

## 7. Your review (2026-10-11) — our answers

1. **Breaking change — agreed.** `metadata.quality` goes and the other `metadata` keys appear only
   with a value; mark it breaking in the 1.5.1 changelog entry despite the patch number.
2. **Two version fields — `technical_details.version` is authoritative.** `version_tracking.obex_version`
   is a second copy the scraper writes from the same scrape; it equals `technical_details.version` in
   all 130 objects (20 carry a value), and nothing reads it. **Removed in KB v1.24.2.** *Superseded
   by KB v1.24.4:* `technical_details.version` is gone too. OBEX publishes no version field, and the
   scraper's values were guesses from the description, three of them a tool's version. There is no
   version field; drop it (§3.2).
3. **The shared spec — updated.** `engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`'s
   `p2kb_obex_get` row now states the 1.5.0 shape and the 1.5.1 contract (breaking, field sources,
   `full_metadata`). Re-import it byte-identical from the KB's `main`; `DOCs/API.md` and
   `docs-src/data/tools.yml` are yours as you said.
4. **2842's cut-off `description_short` ("andthe") — the KB's to fix, no server change.** Our scraper
   builds `description_short` as the first 100 characters of the description, cutting mid-word (50 of
   130 objects), and 2842's also lost a space. **Fixed in KB v1.24.2**: every object now has an
   authored one-line summary there, and the KB's copy of each object mirrors its catalog page (§2).
   Keep reading `functionality.description_short` for `description` exactly as today.
