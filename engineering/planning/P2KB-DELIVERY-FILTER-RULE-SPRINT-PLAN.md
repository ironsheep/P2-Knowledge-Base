# P2KB Delivery-Filter Rule — sprint plan

**Head:** `yaml:p2kb` · **Written:** 2026-10-07 · **Status:** PLANNING — open questions in §0
**Closes:** F-439 (the MCP serves provenance) · **Interface:**
`engineering/tools/p2kb-mcp/MCP-DELIVERY-FILTER-HANDOFF.md` (the agreement with the MCP agent)

**What the sprint is for.** Move the delivery filter's rule out of each receiver and into the
published index, so a rule change reaches every receiver on its next refresh instead of becoming an
escape until each one ships. Receivers keep a fixed engine. **Done** = the KB publishes the rule,
every KB-side receiver and gate reads it from the index, the MCP server matches our reference output
byte for byte on the whole KB, both release (KB first), and the live acceptance probes pass.

**How Stephen wants it run** (2026-10-07): one review round by the MCP agent on the agreement → we
build and certify our side → a test bundle (files, not a commit) that Stephen copies to the MCP
environment → the MCP agent implements and tests against it → iterate with nothing released →
both release on agreement.

---

## 0. Open questions

Asked one at a time; each carries a recommendation.

1. ~~Require `jq` for the bash scripts?~~ **RESOLVED 2026-10-07 — no.** Stephen: *"we can not
   leave any host side dependency."* Research had found the bash scripts already depend on `jq` in
   practice: `fetch-kb-file.sh:139-142` falls back to `grep -o "\"$key\":{\"path\":..."` without
   `jq`, but the generator writes the index pretty-printed (`generate-p2kb-index.py:671`,
   `indent=2`), so the pattern never matches — measured: 0 hits for `"p2kbPasm2Add":{"path"` in both
   `p2kb-index.json` and the `.gz`. **Key lookup without `jq` is broken today.** That is a defect,
   fixed in this sprint (§2a, §3): the bash scripts use **no `jq` at all** — only what they already
   need (`curl`, `gunzip`, `awk`, `grep`, `sed`) — reading an index whose line layout the generator
   guarantees and a release gate proves.
2. **Do any open punch-list / register items join this sprint?** Presented as a group in §0.1.
   **Recommendation:** none — F-545 is the KB-side content work that §8's discipline relies on but
   is independently scoped under its own ruling; F-552 is a content fix in «#387»'s lane.
3. **How is the PowerShell engine verified?** No `pwsh` in this container; the current parity gate
   only checks that field names appear in the `.ps1` text. **Recommendation:** install PowerShell in
   the devcontainer image (`.devcontainer/Dockerfile`, the same place the PDF tools are baked in) so
   the §5 gates run the `.ps1` engine and reader exactly as they run bash. *(Alternative: Stephen
   runs a supplied `.ps1` check on a Windows/macOS host each release — a manual step a gate cannot
   enforce.)*

### 0.1 Open items presented with the scope (unfiltered)

- **Register:** **F-439** (closed by this sprint) · **F-545** provenance under unlisted keys
  (`last_verified`, `extraction_status`, …; ruling 2026-10-04: the list does not grow) · **F-552**
  (filed today): F-387's operator tables ship `(:NNN)` line cites; the existing payload scan fails
  the next release on 33 hits. All other open register findings are KB content («#387»).
- **`engineering/tools/p2kb-mcp/PUNCH-LIST.md`:** **PL-004** part 2 — review the remaining
  `version:` / `last_updated:` bearers against "the KB is always latest".
- **Doc-audit instrument** (`audit-guide-conformance.py --inventory`, run 2026-10-07): 2 findings,
  both outside this sprint's surfaces — `app-notes/APP-NOTE-VOICE-GUIDE.md:185` (restated voice
  rule) and `manuals/p2-errata/creation-guide.md:28` (codename "Silicon Doc").

---

## Standing rulings that bind this sprint

- **2026-10-04, Stephen (F-545):** the filter's key list does not grow — "let's make sure we're using
  existing keys the way we should and not inventing new keys." → agreement §8.4.
- **2026-10-07, Stephen (this planning session):** the published file stays complete, filtering
  happens at the receiver; the rule is published in the index; field names are literals, not regex;
  the rule carries a format number; cache stamp = rule hash + engine version; column-0 comments go as
  a class; fetch scripts fall back **quietly** (no runtime warning — no consumer can act on one);
  `p2kb_version` reporting is a maintainer diagnostic only; our own gates read the rule from the
  index, never a copy; the certification bundle is built from **committed** YAMLs at HEAD, is **not
  committed**, and is **frozen** — findings during certification are registered, never fixed into
  the bundle; release order KB → server.
- **Sacred Rule 1** (backups) for every file >100 lines edited; **no file renames** (the handoff is
  rewritten in place); **stage by explicit path**; no push/release without Stephen.

## Measured premises (2026-10-07, KB HEAD `9e2f7067`)

| Premise | Measurement |
|---|---|
| The format-1 engine (agreement §4) equals today's shipped filter minus the remaining column-0 comments | Python transliteration vs `fetch-kb-file.sh filter_metadata` over all 1,130 live files: **0 mismatches** (throwaway session check; §5's `_predicted_filtered` makes it permanent) |
| Removing **all** column-0 comments is content-safe | 1,342 lines in 175 files; parsed YAML changed in **0** files |
| The payload provenance scan already exists | `validate-dod-release.py:634` `validate_internal_ids` reads the shipped payload; today it **fails, 33 hits** (F-552) |
| Our own receivers carry stale rule copies | `refresh-kb.sh:198-200` and `refresh-kb.ps1:220-226` still run the **original five-field** `grep -v` — the F-439 defect, on our side |
| Bash index lookup without `jq` is broken | §0 Q1 — 0 hits for the fallback's pattern in both index files |
| No PowerShell in the container | `which pwsh powershell` → none |
| Server can be pointed at local files | `P2KB-MCP-SPECIFICATION.md` §Configuration: `P2KB_BASE_URL` — confirmed by the MCP agent in review (agreement §11.1) |
| Live index count | 1,131 entries, 1,130 files present — `op_addlteqgt.yaml` deleted by F-547, index not yet regenerated (expected; the bundle regenerates it) |

---

## 1. The interface agreement — one review round

**Why:** the MCP agent builds against the agreement; it must be settled before either side codes.
**Starting point:** `MCP-DELIVERY-FILTER-HANDOFF.md` rewritten in place 2026-10-07 (backup in
`.backups/`). **Target:** Stephen hands it over; the MCP agent replies once (its §11 questions plus
anything else); we fold the reply in and mark it AGREED. **Verify:** every §11 question answered;
every change from the reply traced to a line of the reply; status line reads AGREED with the date.

## 2. The index carries the rule

**Starting point:** `generate-p2kb-index.py` builds `index` in `generate_index()` and writes it at
`:671`; top-level keys today: `system`, `categories`, `aliases`, `files`.
**Target:** a top-level `delivery_filter` block (agreement §3), defined **once** in the generator as
the single source of the rule; `system.version` bumps (3.5.0 → 3.6.0) and the spec's Index Structure
documents it. The generator prints the `rule_id` (agreement §3.1).
**Verify:** normal — block present, fields sorted, `rule_id` printed and recomputable by hand;
edge — the generator rejects a non-literal field name; error — malformed block cannot be emitted
(the generator validates before writing).

## 2a. The index line layout is a guarantee (no host-side dependency)

**Why:** §0 Q1 — the bash scripts must read the index with no `jq`, and today's no-`jq` paths
silently find nothing. **Starting point:** `json.dump(index, f, indent=2)` (`generate-p2kb-index.py:671`)
— a layout nothing promises. **Target:** the generator writes the index in a fixed, documented line
layout that is still plain valid JSON (the server and PowerShell parse it as JSON, unaffected): one
line per record — the `system` object on one line, the `delivery_filter` object on one line, one
line per category (`"name": [keys]`), per alias (`"ALIAS": [keys]`), and per file
(`"key": {"path": …, "mtime": …, "sha256": …}`), each section opened and closed on its own line. The
layout is written down in the spec's Index Structure section as part of the interface.
**Verify:** normal — `json.load` of the new index equals `json.load` of the old one (same content,
different whitespace); edge — keys containing characters JSON escapes (measure whether any exist and
cover them in the bash reader); error — the §5 reader-parity gate fails on any record the bash
reader misreads.

## 3. The KB reference engine — `fetch-kb-file.sh` and `.ps1`

**Starting point:** `fetch-kb-file.sh:205-232` (`filter_metadata`, awk, hard-coded list and comment
keywords); `fetch-kb-file.ps1:221-260` (`Filter-Metadata`, same); script cache under `.p2kb/cache`
with no rule awareness (`fetch-kb-file.sh:370-395`).
**Target:** both apply format 1 exactly (agreement §4) with the rule read from the cached index
(bash: `awk` over the §2a layout, **no `jq`**; PowerShell: `ConvertFrom-Json`); a built-in format-1
rule used **quietly** when the index has no block or one the script cannot apply; the script cache
stamped with `rule_id` + script version and cleared when it changes. **Every `jq` use in
`fetch-kb-file.sh` (22 lines: lookup, aliases, search, browse, categories, entry count) is replaced
by an `awk` reader of the §2a layout** — one code path, not a `jq` path beside a fallback that can
rot. Script versions bump together (parity gate checks they match).
**Verify:** normal — output equals the Python transliteration on all files; every subcommand
(`<key>`, `--search`, `--browse`, `--categories`, alias lookup) returns what `json.load` of the index
says it should, on a machine path with `jq` absent from `PATH`; edge — index without a block →
built-in rule, same output; a `format: 2` index → built-in rule; changed rule → cache cleared.

## 4. `refresh-kb.sh` / `.ps1` stop carrying their own filter

**Starting point:** `refresh-kb.sh:198-207` and `refresh-kb.ps1:220-236` prefetch common keys through
a stale five-field filter. `refresh-kb.sh:129-133` already downloads `fetch-kb-file.sh`.
**Target:** the refresh scripts prefetch **through** `fetch-kb-file.*` — one engine per language, no
second copy (shared-component rule); `refresh-kb.sh`'s 5 `jq` uses go the same way as §3's.
**Verify:** prefetched cache bodies byte-equal to
`fetch-kb-file.*` output for the same keys; no `filter`/field-name literal left in either refresh
script (grep).

## 5. Release gates read the rule from the index

**Starting point:** `validate-dod-release.py:39-66` hard-codes `FILTER_PATTERN`,
`COMMENT_PROVENANCE_PATTERN`, `EXPECTED_FILTER_FIELDS`; `_predicted_filtered` (`:440`) is the
independent second implementation; `_apply_shipped_filter` (`:478`) runs the bash engine;
`validate_fetch_script_parity` (`:954`) checks field names appear in both scripts' text.
**Target:**
- Every gate takes the rule from the **generated index**; no list in the validator.
- `_predicted_filtered` implements format 1 from the index rule (stays an independent reading).
- `_apply_shipped_filter` runs the bash engine against that same index.
- `validate_internal_ids` (the escape scan, agreement §8.3) is unchanged — it already reads the
  payload. F-552 makes it fail today; that is a register item, not this sprint's.
- New check (reader parity, replaces the fixed-line gate agreed earlier): with `jq` off `PATH`,
  the bash reader recovers the rule (same `rule_id` as the validator) and resolves **every** file
  key, alias and category of the generated index exactly as `json.load` does. A layout change that
  breaks the reader fails the release.
- The PowerShell engine cannot run in this container (no `pwsh` — measured 2026-10-07); how it is
  verified is §0 Q3.
- `validate_fetch_script_parity` checks the scripts' **built-in** fallback rules equal the index rule,
  not that field names appear in their text.
**Verify:** normal — all filter gates green on HEAD except the known F-552 scan; edge — a doctored
index rule changes what every gate expects (proves nothing reads a copy); error — an index with no
block fails the release (agreement §8.1).

## 6. Golden vectors

**Starting point:** `engineering/tools/p2kb-mcp/filter-test-vectors/input.yaml` / `expected.yaml`
(md5s in the old handoff), built for the keyword-comment rule.
**Target:** `expected.yaml` regenerated by running the §3 engine (never hand-written), with cases
added: a non-provenance column-0 comment (now removed), a column-0 comment inside a span, `#` with no
space, an indented `#` outside a span (kept). **Verify:** the Python transliteration and both script
engines produce `expected.yaml` byte for byte.

## 7. Certification bundle builder

**Requested by Stephen** (2026-10-07: "you create test files — no commit — I copy to other
environment, they test"). **Target:** `engineering/tools/p2kb-mcp/build-filter-cert-bundle.py`
producing the layout in agreement §9.1 into a git-ignored directory
(`engineering/tools/p2kb-mcp/cert-bundle/`, new `.gitignore` rule), from `git ls-files` content at
HEAD (refuses a dirty `deliverables/ai/P2/` tree), with expected outputs produced by the §3 bash
engine, both variants, the no-block command in the README, and `MANIFEST.sha256`.
**Verify:** normal — manifest checks; `expected/` count = index entries; each `serve/` YAML's git-blob
hash equals its index `sha256`; edge — variant B's expected set differs from main exactly where B's
rule differs; error — dirty tree → refuses.

## 8. Certification run and iteration

Stephen copies the bundle; the MCP agent runs agreement §9.2 and reports per §9.3. A mismatch is
diagnosed against **both** engines before either is changed; if ours changes, §6/§7 rerun and a new
bundle goes over. The bundle's KB content is frozen at the recorded HEAD — content findings go to the
register. **Verify:** all five §9.2 steps pass on the MCP side, reported with the server version.

## 9. Release and acceptance

KB release first (`release-yamls`), which requires the payload scan green — i.e. **F-552 fixed by
then** (register work, not this sprint); then the server release; then agreement §10.3 live probes;
F-439 closed in the register with the server version.

## 10. Documentation

- `P2KB-MCP-SPECIFICATION.md` — §Index Structure (`delivery_filter`, 3.6.0), §Content Filtering and
  §Filter Implementation (point to the agreement; drop the hard-coded list and keyword comment rule),
  §Cache Invalidation (rule stamp), `p2kb_version` (diagnostic fields).
- `MCP-DELIVERY-FILTER-HANDOFF.md` — status → AGREED; outcome noted at release.
- `engineering/tools/p2kb/METADATA-FILTER-DESIGN.md` — stale (v3.0, four fields, `grep -v`): rewrite
  to the current design, pointing at the agreement as canonical.
- `engineering/procedures/yaml-workflow-quick-guide.md:121-131` — stale "5 fields" section: replace
  with a pointer to the rule in the generator.
- `.claude/skills/release-yamls/SKILL.md` — name the new rule read-back check among the gates it runs.
- Spec §Index Structure — the §2a line layout, stated as part of the interface.
- KB CHANGELOG entry at the release.

## Documentation Blast Radius

Behaviors changed: what is removed at delivery (all column-0 comments now), where the rule lives
(index), the index's line layout (now guaranteed), bash scripts working without `jq`, cache
invalidation, gate inputs.

| Artifact | Describes | Disposition |
|---|---|---|
| `P2KB-MCP-SPECIFICATION.md` §§ Index Structure, Content Filtering, Filter Implementation, Cache Invalidation, `p2kb_version` | rule, engine, cache | §10 |
| `MCP-DELIVERY-FILTER-HANDOFF.md` | the interface | rewritten 2026-10-07 (§1) |
| `engineering/tools/p2kb/METADATA-FILTER-DESIGN.md` | filter design — **already stale** | §10 |
| `engineering/procedures/yaml-workflow-quick-guide.md:121-131` | field list — **already stale** | §10 |
| `fetch-kb-file.sh/.ps1` header comments (`:195-204`) | rule rationale, "61 files carry one" | §3 |
| `validate-dod-release.py` docstrings (`:39-66`, `:440-500`, `:954`) | rule copies | §5 |
| `.claude/skills/release-yamls/SKILL.md` | gate list | §10 |
| `deliverables/ai-reference/BOOTSTRAP.md`, `README.md`, `CLAUDE-QUICKSTART.md` | script usage | checked — none states a `jq` prerequisite; nothing to change |
| `deliverables/ai-reference/auxiliary-guides/interaction/using-with-ai.md:108,175` | suggests `jq` **or** grep to the reader for ad-hoc index search | none — an optional reader tip, not a script dependency |
| `filter-test-vectors/` + md5s quoted in docs | expected output | §6 |
| `P2KB-CORRECTION-FINDINGS.md` F-439, F-552 | status | §9 / filed |
| Counts: "1,131 files", "61 files carry one", "141 block scalars" | measurements | re-measured where restated |
| Historical docs (`engineering/analysis/2026-08-27-*`, `operations/sprints/dod-v3-sprint-plan.md`) | past state | none — dated records, not current-state docs |

Doc-audit instrument output: §0.1 (2 findings, outside this sprint's surfaces).

## Exit gate — coverage

1. **Standing rulings** — quoted above with dates.
2. **Intent** — stated at top, from Stephen's 2026-10-07 direction.
3. **Decisions and open items** — every agreed point maps to agreement §§3-10 and plan §§2-9; open
   items listed in §0.1 awaiting his disposition (Q2).
4. **Premises** — measured, table above; `P2KB_BASE_URL` coverage is the one premise only the MCP
   agent can confirm (agreement §11.1).
5. **Research** — the defect class (a receiver holding a rule copy) searched across the repo: found
   in `refresh-kb.*` (§4) and the validator (§5), not only the server. No bench work.
6. **Named unknowns** — the MCP agent's review reply (§1) may change the agreement; the plan
   absorbs it as a dated revision. Whether the server's `P2KB_BASE_URL` covers manifests (§11.1) —
   if not, the bundle adds what it needs.

Questions remaining: §0 Q2, Q3 (Q1 resolved 2026-10-07).
