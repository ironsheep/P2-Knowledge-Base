# Delivery Filter Design

*Rewritten 2026-10-07. The earlier "v3.0" design (four fields, a `grep -v`) is in git history.*

## Purpose

Every KB file carries **provenance** — how this project knows a claim is true: `source:` /
`sources:` fields, bench-ledger ids, repo paths, editorial timestamps. The KB's release gates
and auditors read it; a code-generating agent can act on none of it. It stays in the published
files (they are the traceable record) and is removed **at delivery, by each receiver**.

## The canonical definition

`engineering/tools/p2kb-mcp/MCP-DELIVERY-FILTER-HANDOFF.md` — the interface agreement with the
p2kb-mcp server (AGREED 2026-10-07). It defines the rule block, the format-1 engine, how a
receiver chooses the rule in effect, the cache stamp and certification. This page summarizes;
the agreement governs.

## Rule published, engine fixed

- **The rule** lives in one place — `DELIVERY_FILTER` in `engineering/tools/generate-p2kb-index.py`
  — and is published in every index as the `delivery_filter` block (index schema 3.6.0): literal
  field names to remove, and whether to remove column-0 comments.
- **The engine** is fixed and carried by every receiver: `filter_metadata` in
  `fetch-kb-file.sh`, `Filter-Metadata` in `fetch-kb-file.ps1`, and the server's Go
  implementation. A rule change reaches all of them on their next index refresh; only an engine
  change needs new receiver code.
- **Built-in fallback:** each receiver also carries the current rule as a built-in, used quietly
  when the index has no usable block (and, in the bash script, when `jq` is not installed).
- **Cache:** cached bodies are stamped `rule_id/engine-version` and discarded when the stamp
  changes or is missing.

## The engine in one paragraph

A line rule, indentation-aware — not a YAML-aware key delete and not a plain `grep -v`. A line
whose text after its indentation is a listed name followed immediately by `:` is removed, and so
is every following line indented deeper than it (a block scalar, a nested map or list) plus blank
and comment-only lines inside that span. Column-0 `#` lines are removed as a class. Content that
merely uses the word stays: `- source:` and `{source: ...}` do not match. Exact semantics, edge
cases and the Go reference: the agreement, §4.

## Where it is checked

`engineering/tools/validate-dod-release.py`, at every release, reading the rule from the
generated index:

- **Metadata Filter** — the shipped bash engine against an independent transcription of the
  agreement, on every file; the filtered payload must still parse and lose no content.
- **Internal IDs in Shipped Content** — the filtered payload carries no bench/finding id, repo
  path or `file:line` citation (provenance that escaped the rule).
- **Fetch Script Parity** — both scripts' built-in rules equal the index rule.
- **Filter Rule Read-Back** — `fetch-kb-file.sh` reads the published rule back.
- **No-jq Key/Alias Lookup** — without `jq`, every key and alias resolves as `json.load` reads it.
- **PowerShell Filter Verified** — the `.ps1` scripts are the versions verified on Windows
  (`PS1-VERIFIED.md`, `verify-ps1-filter.ps1`).

Golden vectors for any implementation: `engineering/tools/p2kb-mcp/filter-test-vectors/`.
