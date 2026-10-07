# P2KB MCP Server Specification

*The interface between the P2 Knowledge Base and the `p2kb-mcp` server*

**Status — where we are, 2026-10-07.** This document states the interface as it stands today and
marks what is **agreed but not yet built**. Live facts were read from the server itself on
2026-10-07 (`p2kb_version`: `mcp_version` 1.4.0, index 3.5.0, 1,131 entries) and from the MCP agent's
review of the delivery-filter agreement the same day.

**Companion documents (this folder):**
- `MCP-DELIVERY-FILTER-HANDOFF.md` — the **delivery-filter interface agreement** (AGREED 2026-10-07).
  It is canonical for the rule, the engine, rule resolution, the cache stamp, the new
  `p2kb_version` fields and certification. This spec points to it rather than repeating it.
- `OBEX-IMPLEMENTATION-SPEC.md` — the OBEX tools.
- The original 2025 design (repository layout, dev container, CI, build targets, issue templates,
  the first tool list) is this file as of commit `804715b7` —
  `git show 804715b7:engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`. Superseded as a
  statement of the interface; kept as history. The server's own repository owns its implementation
  details.

**Where this spec and the agreement differ, the agreement wins.**

---

## 1. Overview

The server gives AI agents structured access to the P2 Knowledge Base without shell scripts. The KB
publishes an index and YAML files on GitHub; the server fetches, verifies, filters, caches and
serves them through MCP tools. The KB's fetch scripts (`engineering/tools/p2kb/fetch-kb-file.sh` /
`.ps1`) are the other receiver of the same files and apply the same filter.

```
Agent                     p2kb-mcp server                         GitHub (KB repo, main)
┌─────────┐  MCP call     ┌──────────────────────────┐  HTTP GET   ┌───────────────────────────┐
│         │ ────────────► │ index manager            │ ──────────► │ p2kb-index.json.gz        │
│         │ ◄──────────── │ hash check → filter →    │ ◄────────── │ deliverables/ai/P2/**.yaml│
└─────────┘  results      │ cache → tools            │             └───────────────────────────┘
                          └──────────────────────────┘
```

## 2. Data sources

Base URL: `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main` (overridable with
`P2KB_BASE_URL` — **agreed, not yet implemented**; §8).

| Resource | Path under the base | Purpose |
|---|---|---|
| Index | `deliverables/ai/p2kb-index.json.gz` | keys → paths, categories, aliases, hashes; from KB 3.6.0 also the delivery-filter rule |
| KB files | `deliverables/ai/P2/<path>` (the index entry's `path`) | content — including the OBEX object YAMLs under `community/obex/objects/` |

The server fetches **nothing else** from the KB (MCP agent, 2026-10-07). The original design listed
`manifests/propeller-knowledge-root.yaml` and `manifests/ai-instructions.yaml`; the server does not
use them.

## 3. Index structure

```json
{
  "system": {
    "version": "3.5.0",
    "generated": "2026-10-04T18:47:24.835817",
    "total_entries": 1131,
    "total_categories": 59,
    "total_aliases": 3091,
    "multi_target_aliases": 189,
    "source": "deliverables/ai/P2/"
  },
  "delivery_filter": { "format": 1, "remove_fields": [ ... ], "remove_column0_comments": true },
  "categories": { "pasm2_branch": ["p2kbPasm2Call", "p2kbPasm2Jmp", ...], ... },
  "aliases":    { "ABS": ["p2kbPasm2Abs", "p2kbSpin2Abs"], ... },
  "files": {
    "p2kbPasm2Mov": {
      "path": "deliverables/ai/P2/language/pasm2/mov.yaml",
      "mtime": 1783740381,
      "sha256": "1d596fed3283290cbe1582823b89e6b1d058eaac31af5a625d5fb629be5cb2ed"
    },
    ...
  }
}
```

- **`files`** (not `entries`) — one entry per KB file, including the 131 OBEX object files
  (`p2kbCommunity<id>` keys, `_template.yaml` among them).
  - `path` — repo-relative; fetch from `<base>/<path>`.
  - `mtime` — committer timestamp of the file's last commit (`git log -1 --format=%ct`).
  - `sha256` — SHA-256 of the file's **committed git blob bytes**, exactly what the raw URL serves.
    Hash the raw HTTP body **before** filtering and compare; a mismatch is a stale or poisoned body →
    re-fetch.
- **`aliases`** — alias → array of target keys. Lookups search aliases as well as `files` keys,
  resolving and de-duplicating targets.
- **`delivery_filter`** — **agreed, appears from index schema 3.6.0** (the first KB release after
  2026-10-07). The rule receivers apply. Absent in 3.5.0 and earlier. Format, validation and
  `rule_id`: agreement §3.
- `system.version` is the index schema version (3.5.0 today → 3.6.0 with `delivery_filter`).

## 4. Content filtering

Every KB file carries **provenance** — `source:` / `sources:` fields, bench-ledger ids, repo paths,
line citations. The KB's release gates read it; a consuming agent can act on none of it. It is
removed at delivery, by the receiver, from **every file fetched from `deliverables/ai/P2/`** (OBEX
objects included) before the file is parsed, cached or returned.

**The rule is published in the index; the server carries only the engine.** Everything about it —
the rule block, the format-1 engine and its Go reference, the built-in rule, how the rule in effect
is chosen, empty input, exactness details — is in the agreement, §§3–5.

**Today (2026-10-07)** the live server still applies its original five-field regex, so `sources:`
blocks and provenance comments reach agents (register finding **F-439**). The agreement replaces that
filter entirely; F-439 closes when the agreement's live acceptance (§10) passes.

## 5. Tools — as served today

Read from the live server's tool schemas, 2026-10-07. Every tool description begins by naming the KB
as the authoritative P2 source.

| Tool | Parameters | What it does |
|---|---|---|
| `p2kb_get` | `query` (string, required) — natural language or an exact key | Returns one KB entry's content plus related items; ambiguous queries return suggestions. The result is JSON; the YAML is in its **`content`** field. |
| `p2kb_find` | `term`, `category` (strings, optional), `limit` (int, default 50) | No parameters: categories with counts. `term`: matching keys. `category`: keys in that category. |
| `p2kb_refresh` | `flush` (bool, default false), `include_obex` (bool, default false) | Re-fetches the index and removes stale cache entries by index timestamps; `flush` wipes the whole content cache; `include_obex` also refreshes OBEX. |
| `p2kb_version` | none | Diagnostic: `mcp_version`, `index_version`, index status (`total_entries`, `total_categories`, `total_aliases`, cache age), OBEX cache status. **Agreed additions** (not yet built): `filter_rule_id`, `filter_rule_source`, `filter_engine_version`, `filter_rule_refused` — agreement §7. |
| `p2kb_obex_get` | `query` (string, required) — search text or numeric object id | One OBEX object's metadata with download URL and instructions. |
| `p2kb_obex_find` | `term`, `category`, `author` (strings, optional), `limit` (int, default 20) | Browse/search OBEX objects. |
| `p2kb_obex_download` | `object_id` (string, required), `target_dir` (optional) | Downloads and extracts an OBEX object (default `./OBEX/<id>-<slug>/`). |

The original design's `p2kb_search`, `p2kb_browse`, `p2kb_categories`, `p2kb_batch_get`,
`p2kb_info`, `p2kb_stats`, `p2kb_related` and `p2kb_help` are not part of the interface; `p2kb_get`
and `p2kb_find` cover their roles.

## 6. Cache — interface requirements

The cache's layout and timings are the server's business. What the interface requires:

- **Hash, then filter, then cache.** Only filtered bodies are cached, each under the rule in effect.
- **Per-entry invalidation** when the index's `mtime` / `sha256` for an entry changes.
- **Cache stamp = `rule_id` + `/` + engine version** — **agreed, not yet built**. Checked at startup
  and after every index load or refresh; a different or missing stamp discards every cached body.
  Agreement §6.
- **Last-good rule** persisted beside the cached index — **agreed, not yet built**. Agreement §5.

## 7. Release coupling

- The KB changes the rule **only in a KB release**, and every release index carries it (from 3.6.0).
  Each KB release gate applies the published rule to every file and fails on over-removal, on
  provenance markers in the output, or on its own scripts failing to read the rule back
  (agreement §8).
- A rule change needs **no server release**: the server picks it up on its next index refresh. A
  server release is needed only when the engine changes, and that is certified first (agreement §9).
- Order for the change now in flight: KB release first, then the server, then live acceptance
  (agreement §10).

## 8. Configuration

| Variable | Status | Meaning |
|---|---|---|
| `P2KB_BASE_URL` | **agreed, not yet implemented** (MCP agent, 2026-10-07) | Replaces the base URL for the index and file fetches (agreement §9.2). |

Other server settings (cache location, index TTL, logging) belong to the server and are documented
in its repository; the original design's proposals are in commit `804715b7` (see the top).

## 9. Testing and certification

The engine is certified against a KB-built bundle — the whole KB with expected filtered output,
golden vectors, rule variants — before either side releases: agreement §9. Live acceptance after
release: agreement §10.

## 10. Open with the MCP agent

Items this spec states from the agreement or the original design and that the server side should
confirm or correct:

1. The two contract changes made after the agreement's review: a **missing** rule block falls back
   to last-good (not straight to built-in), and rule parsing is **strict** (agreement §§3, 5).
2. That the OBEX tools read the object YAMLs through the same fetch path, so §4's filter covers them.
3. The `p2kb_get` result's other fields (beyond `content`), if the KB's acceptance probes should read
   them.
