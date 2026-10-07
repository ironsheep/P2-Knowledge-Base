# P2KB Delivery-Filter Rule — sprint plan

**Head:** `yaml:p2kb` · **Written:** 2026-10-07 · **Status:** READY — agreement AGREED 2026-10-07 (§1 done); next: `plan-to-tasks`

**Revisions**
- 2026-10-07 — MCP review folded in: engine step 1 (a comment inside a span no longer ends it),
  empty input → empty output, cache stamp checked at startup and unstamped caches discarded (all
  three receivers, §3); no `manifests/` in the bundle; comparisons on the `p2kb_get` `content` field;
  `P2KB_BASE_URL` is implemented by the server in this work, not already present. **Cause: 2 —
  research incomplete** (the engine text was not exercised against a comment-inside-span or an empty
  input before it was sent, and the spec's `P2KB_BASE_URL` / manifests claims were taken from the
  spec, not confirmed).
- 2026-10-07 — the spec update moves from §10 (at release) to new §1a (now, delivered to the MCP
  agent as the current-state document beside the agreement). **Cause: 1 — owner ruling not asked
  for** (when the spec should be current, and who receives it, was not asked at planning).

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

1. **RESOLVED 2026-10-07 — the `jq` arrangement does not change.** The bash scripts keep using `jq`
   when present and falling back without it; no new host-side dependency. The rule needs no `jq`-less
   reader at all: with `jq` the script reads the index's rule; without it, it uses its built-in rule
   (the quiet fallback already agreed).
1a. **RESOLVED 2026-10-07 — fix the broken no-`jq` fallback in this sprint (§3a).** Found while
   researching: `fetch-kb-file.sh:139-142` falls back to `grep -o "\"$key\":{\"path\":..."`, but the
   generator writes the index pretty-printed (`generate-p2kb-index.py:671`, `indent=2`), so the
   pattern never matches — measured: 0 hits for `"p2kbPasm2Add":{"path"` in both `p2kb-index.json`
   and the `.gz`. Without `jq`, key lookup finds nothing today. Stephen chose option (a): repair the
   fallbacks in this sprint and gate them.
2. **RESOLVED 2026-10-07 — no open punch-list / register item joins this sprint** (§0.1 list
   presented; Stephen: "none"). F-552 stays in «#387» and must be fixed before §9's KB release.
3. **RESOLVED 2026-10-07 — PowerShell is verified once, by Stephen, and again only if the `.ps1`
   changes.** Stephen: the scripts run only on Windows (his Windows emulator on macOS) — *"let's do
   as little of this as possible."* The design makes that enough: the engine is fixed and the rule
   comes from the index, so a rule change needs no Windows run. Mechanism (§5b): one supplied check
   script, run once this sprint; the release gate pins the hashes of the two `.ps1` files to the last
   recorded Windows pass and fails if either changes without a new one.

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
| The format-1 engine (agreement §4) equals today's shipped filter minus the remaining column-0 comments | Draft engine: Python transliteration vs `fetch-kb-file.sh filter_metadata` over all 1,130 live files: **0 mismatches**. Agreed engine (comment-in-span fix): differs from the draft on **2 files**, `spin2-language-schema.yaml` (1 line) and `spin2-builtin-symbols-complete.yaml` (9 lines) — indented maintainer comments inside a span, no content (throwaway session checks; §5's `_predicted_filtered` makes it permanent) |
| Removing **all** column-0 comments is content-safe | 1,342 lines in 175 files; parsed YAML changed in **0** files |
| The payload provenance scan already exists | `validate-dod-release.py:634` `validate_internal_ids` reads the shipped payload; today it **fails, 33 hits** (F-552) |
| Our own receivers carry stale rule copies | `refresh-kb.sh:198-200` and `refresh-kb.ps1:220-226` still run the **original five-field** `grep -v` — the F-439 defect, on our side |
| Bash index lookup without `jq` is broken | §0 Q1a — 0 hits for the fallback's pattern in both index files |
| No PowerShell in the container | `which pwsh powershell` → none |
| Server can be pointed at local files | **Not today** — the spec lists `P2KB_BASE_URL` but the server does not implement it (MCP agent, 2026-10-07); the server implements it for index + content in this work. It fetches no `manifests/` |
| Live index count | 1,131 entries, 1,130 files present — `op_addlteqgt.yaml` deleted by F-547, index not yet regenerated (expected; the bundle regenerates it) |

---

## 1. The interface agreement — one review round — DONE 2026-10-07

**Outcome:** the MCP agent agreed the design and asked for three engine changes plus answered §11;
all folded in (see Revisions); the agreement reads AGREED. **Why:** the MCP agent builds against the agreement; it must be settled before either side codes.
**Starting point:** `MCP-DELIVERY-FILTER-HANDOFF.md` rewritten in place 2026-10-07 (backup in
`.backups/`). **Target:** Stephen hands it over; the MCP agent replies once (its §11 questions plus
anything else); we fold the reply in and mark it AGREED. **Verify:** every §11 question answered;
every change from the reply traced to a line of the reply; status line reads AGREED with the date.

## 1a. Bring `P2KB-MCP-SPECIFICATION.md` to "where we are today" — delivered to the MCP agent

**Requested by Stephen** (2026-10-07): update the spec so it can go to the MCP agent as the
current-state document alongside the agreement. Done **before** either side builds, not at release.
**Starting point:** `engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md` (1,409 lines — backup
first). Known-wrong or superseded today:
- §Data Sources (`:43-54`) lists `manifests/` fetches — the server fetches none (MCP agent).
- §Index Structure (`:56-97`) — no `delivery_filter`; schema 3.5.0.
- §Content Filtering (`:98-152`) — hard-coded nine-field list, keyword comment rule, and an
  "ungated third implementation / F-439" warning that this agreement retires.
- §Filter Implementation (`:620-684`) — the old `FilterMetadata` reference.
- §Cache Invalidation on Index Update (`:460-470`) — no rule stamp, no startup check.
- `p2kb_version` (`:279-293`) — no filter fields.
- §Configuration (`:1000-1011`) — presents `P2KB_BASE_URL` as existing; it is not implemented yet.
- Any other statement a read-through finds false against the server as the MCP agent describes it
  or against the agreement.
**Target:** every section above states the agreed interface and the server's actual current state;
the filter sections **point to the agreement** as canonical (rule, engine, resolution order, cache
stamp, `p2kb_version` fields) instead of restating the engine, so there is one copy. Where something
is agreed but not yet built (`P2KB_BASE_URL`, the filter fields), the spec says so plainly. A dated
status line at the top says what the document reflects. Stephen hands it to the MCP agent with the
agreement.
**Verify:** normal — every section listed above changed and re-read against the agreement; edge —
no remaining copy of the field list or engine code outside the agreement (grep the spec for
`source_reference`, `FilterMetadata`, `Extracted from`); error — any claim the KB cannot confirm
about the server is phrased as the MCP agent stated it, with the date, or flagged for them.

## 2. The index carries the rule

**Starting point:** `generate-p2kb-index.py` builds `index` in `generate_index()` and writes it at
`:671`; top-level keys today: `system`, `categories`, `aliases`, `files`.
**Target:** a top-level `delivery_filter` block (agreement §3), defined **once** in the generator as
the single source of the rule; `system.version` bumps (3.5.0 → 3.6.0) and the spec's Index Structure
documents it. The generator prints the `rule_id` (agreement §3.1).
**Verify:** normal — block present, fields sorted, `rule_id` printed and recomputable by hand;
edge — the generator rejects a non-literal field name; error — malformed block cannot be emitted
(the generator validates before writing).

## 3. The KB reference engine — `fetch-kb-file.sh` and `.ps1`

**Starting point:** `fetch-kb-file.sh:205-232` (`filter_metadata`, awk, hard-coded list and comment
keywords); `fetch-kb-file.ps1:221-260` (`Filter-Metadata`, same); script cache under `.p2kb/cache`
with no rule awareness (`fetch-kb-file.sh:370-395`).
**Target:** both apply format 1 exactly (agreement §4). The rule comes from the cached index — bash
via `jq` when present, PowerShell via `ConvertFrom-Json`; a built-in format-1 rule is used
**quietly** when bash has no `jq`, or the index has no block, or one the script cannot apply. The
script cache is stamped with `rule_id` + script version, checked whenever the script determines the
rule in effect (every run, not only on index refresh), and cleared when it differs **or is absent**
(clears caches filtered by older script versions). Empty input → empty output. Script versions
bump together (parity gate checks they match).
**Verify:** normal — output equals the Python transliteration on all files; edge — no `jq` →
built-in rule, same output on today's rule; index without a block → built-in rule; a `format: 2`
index → built-in rule; changed rule → cache cleared.

## 3a. Repair the no-`jq` fallbacks in the bash scripts

**Why:** §0 Q1a. **Starting point:** the `grep`/`sed` fallbacks in `fetch-kb-file.sh` — key lookup
`:142`, alias lookup `:163`, key search `:183`, `:361` — and `refresh-kb.sh:190-194`; they assume
compact JSON. `--browse` / `--categories` (`:291`, `:308`) refuse without `jq`.
**Target:** every fallback reads the index as `json.dump(..., indent=2)` actually writes it, so a
user without `jq` gets the same answers as with it. Whether `--browse` / `--categories` gain a
fallback or keep their explicit "jq required" message is decided at task time against what the
pretty layout allows — the message is honest, a silent miss is not.
**Verify:** normal — with `jq` off `PATH`, key lookup, alias lookup and search return what
`json.load` of the index says for **every** key and alias (the §5 gate); edge — aliases mapping to
several targets, keys that are prefixes of other keys; error — a key not in the index reports
not-found, never a partial match.

## 4. `refresh-kb.sh` / `.ps1` stop carrying their own filter

**Starting point:** `refresh-kb.sh:198-207` and `refresh-kb.ps1:220-236` prefetch common keys through
a stale five-field filter. `refresh-kb.sh:129-133` already downloads `fetch-kb-file.sh`.
**Target:** the refresh scripts prefetch **through** `fetch-kb-file.*` — one engine per language, no
second copy (shared-component rule).
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
- New check (rule read-back): bash with `jq` recovers the index rule and computes the same
  `rule_id` as the validator.
- New check (no-`jq` fallback parity, §3a): with `jq` off `PATH`, the bash fallbacks resolve
  **every** key and alias of the generated index exactly as `json.load` does. A generator layout
  change that breaks the fallbacks fails the release.
- The PowerShell engine cannot run in this container (no `pwsh` — measured 2026-10-07); see §5b.
- `validate_fetch_script_parity` checks the scripts' **built-in** fallback rules equal the index rule,
  not that field names appear in their text.
**Verify:** normal — all filter gates green on HEAD except the known F-552 scan; edge — a doctored
index rule changes what every gate expects (proves nothing reads a copy); error — an index with no
block fails the release (agreement §8.1).

## 5b. PowerShell — one Windows run, then a hash pin

**Why:** §0 Q3. **Target:** a single `.ps1` check (`engineering/tools/p2kb/verify-ps1-filter.ps1`)
that Stephen runs once on Windows. It needs no network: it reads the golden vectors and a small
local index fixture (rule present / absent / `format: 2`), runs `Filter-Metadata` and the rule
reader, and prints one PASS/FAIL line plus the two `.ps1` file hashes. The result is recorded in
`engineering/tools/p2kb/PS1-VERIFIED.md` (date, hashes, PASS). The release gate then fails if
either `.ps1` file's hash differs from the recorded pass — so Stephen runs it again only when a
`.ps1` actually changes, never for a rule change.
**Verify:** normal — Stephen's run prints PASS and the hashes are recorded; edge — editing either
`.ps1` makes the gate fail until re-run; error — a FAIL line names the vector or fixture that
differed.

## 6. Golden vectors

**Starting point:** `engineering/tools/p2kb-mcp/filter-test-vectors/input.yaml` / `expected.yaml`
(md5s in the old handoff), built for the keyword-comment rule.
**Target:** `expected.yaml` regenerated by running the §3 engine (never hand-written), with cases
added: a non-provenance column-0 comment (now removed); comment-only lines (column 0 and indented)
inside a span **followed by more of that field's lines** (all removed — the MCP review case); `#`
with no space; an indented `#` outside a span (kept). Plus a separate empty-input vector pair
(zero bytes → zero bytes). **Verify:** the Python transliteration and both script
engines produce `expected.yaml` byte for byte.

## 7. Certification bundle builder

**Requested by Stephen** (2026-10-07: "you create test files — no commit — I copy to other
environment, they test"). **Target:** `engineering/tools/p2kb-mcp/build-filter-cert-bundle.py`
producing the layout in agreement §9.1 into a git-ignored directory
(`engineering/tools/p2kb-mcp/cert-bundle/`, new `.gitignore` rule), from `git ls-files` content at
HEAD (refuses a dirty `deliverables/ai/P2/` tree), with expected outputs produced by the §3 bash
engine, both variants, the no-block command in the README, and `MANIFEST.sha256`. `serve/` holds
the index and YAMLs only (no `manifests/` — the server fetches none).
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

- `P2KB-MCP-SPECIFICATION.md` — done early, in §1a; re-checked here at release.
- `MCP-DELIVERY-FILTER-HANDOFF.md` — AGREED 2026-10-07; outcome noted at release.
- `engineering/tools/p2kb/METADATA-FILTER-DESIGN.md` — stale (v3.0, four fields, `grep -v`): rewrite
  to the current design, pointing at the agreement as canonical.
- `engineering/procedures/yaml-workflow-quick-guide.md:121-131` — stale "5 fields" section: replace
  with a pointer to the rule in the generator.
- `.claude/skills/release-yamls/SKILL.md` — name the new rule read-back check among the gates it runs.
- KB CHANGELOG entry at the release.

## Documentation Blast Radius

Behaviors changed: what is removed at delivery (all column-0 comments now), where the rule lives
(index), bash key/alias lookup working without `jq` (repaired), cache
invalidation, gate inputs.

| Artifact | Describes | Disposition |
|---|---|---|
| `P2KB-MCP-SPECIFICATION.md` §§ Index Structure, Content Filtering, Filter Implementation, Cache Invalidation, `p2kb_version`, Data Sources, Configuration | rule, engine, cache; two claims the MCP agent says are false today | §1a (early, delivered to the MCP agent) |
| `MCP-DELIVERY-FILTER-HANDOFF.md` | the interface | AGREED 2026-10-07 (§1) |
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
3. **Decisions and open items** — every agreed point maps to agreement §§3-10 and plan §§2-9; §0.1
   items dispositioned by Stephen (none join).
4. **Premises** — measured, table above; the MCP-side premises (`P2KB_BASE_URL`, manifests) were
   answered by the MCP agent's review.
5. **Research** — the defect class (a receiver holding a rule copy) searched across the repo: found
   in `refresh-kb.*` (§4) and the validator (§5), not only the server. No bench work.
6. **Named unknowns** — what the certification run (§8) finds; a mismatch is diagnosed against both
   engines and absorbed as a dated revision if the agreement changes.

Questions remaining: none (Q1, Q1a, Q2, Q3 resolved 2026-10-07).
