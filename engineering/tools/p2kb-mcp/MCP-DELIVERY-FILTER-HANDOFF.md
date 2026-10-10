# P2KB ↔ p2kb-mcp — delivery-filter interface agreement

**Between:** the P2-Knowledge-Base YAML head (the KB) and the agent maintaining
`P2-Knowledge-Base-MCP` (the `p2kb-mcp` server).
**Status:** **AGREED 2026-10-07.** The MCP agent reviewed the draft once (2026-10-07); its three
engine changes (§4 step 1, empty input, startup cache check) and its §11 answers are folded in
below. Both sides build against this text.
**Supersedes:** the 2026-10-04 handoff of the same name (a fixed field list copied into each
receiver). Closes register finding **F-439** when §10 completes.
**Plan on the KB side:** `engineering/planning/P2KB-DELIVERY-FILTER-RULE-SPRINT-PLAN.md`.

---

## 1. Why the interface changes

Every KB entry carries **provenance** — `source:` / `sources:` fields, bench-ledger ids, repo paths,
line citations. Our release gates read it; a code-generating agent can act on none of it. So it is
removed at delivery, by each receiver.

The defect behind F-439 was not a wrong list. It was that **each receiver held its own compiled copy
of the rule**. When the KB changed where provenance lives, it updated its own scripts; the server
kept running its old copy until someone noticed. Any receive-side rule held as a copy has that
timing problem built in: every rule change is an escape until every receiver ships.

**The fix: the rule is published with the content.** The index carries the rule; receivers carry
only a fixed engine that applies it. A rule change reaches every receiver on its next index refresh.

## 2. Who owns what

| | The KB | The server |
|---|---|---|
| The rule (which fields, comment handling) | **Owns.** Publishes it in every release index (§3). Changes it only in a KB release. | Reads it at startup and on every index load/refresh (§5). Never edits or extends it. |
| The engine (how a rule is applied) | Owns the reference implementation and the test bundle (§9). | Implements format 1 exactly (§4). |
| Escapes (provenance the rule does not catch) | **Owns.** Its release gate scans the filtered output of every file (§8). | — |
| Cache correctness | — | Owns: stamp by rule + engine (§6). |

## 3. The rule block in the index

`deliverables/ai/p2kb-index.json` (and the `.json.gz` the server fetches) gains one top-level key:

```json
"delivery_filter": {
  "format": 1,
  "remove_fields": [
    "documentation_level", "documentation_source", "enhancement_source", "last_updated",
    "manual_extraction_date", "scrape_tracking", "source", "source_reference", "sources",
    "verified_against"
  ],
  "remove_column0_comments": true
}
```

- `format` — integer. This agreement defines **format 1** only.
- `remove_fields` — **literal key names, matched exactly and case-sensitively.** Each matches
  `^[A-Za-z0-9_]+$`; no name appears twice; the list is not empty. Not patterns, not regex: Go RE2,
  awk ERE and .NET regex differ, and a list of literals behaves the same everywhere. The KB emits them
  sorted; receivers use them as given.
- `remove_column0_comments` — boolean.
- **All three keys are required, with exactly these types, and a format-1 block has no other keys.**
  A missing key, a wrong type, an extra key, a duplicate or invalid name, or an empty list makes the
  block **refused** (§5) — never "read with defaults". (In Go, a missing boolean decodes silently as
  `false`, which would filter less; §4.1's `ParseRule` guards against that.)
- Every other index key is unchanged (`system`, `categories`, `aliases`, `files`, `sha256`
  semantics). An index without `delivery_filter` is valid (every KB release before this change) —
  see §5.

### 3.1 Rule identity — `rule_id`

Every receiver computes the same identity for a rule, so caches and diagnostics can compare them:

```
rule_id = lowercase hex SHA-256 of the UTF-8 text:
  "p2kb-delivery-filter\n"
  "format=<format>\n"
  "remove_fields=<names joined by ',' in the order the index lists them>\n"
  "remove_column0_comments=<true|false>\n"
```

The KB's release gate computes it from the index it publishes and prints it; the certification
bundle's README states it for every rule in the bundle (§9).

**The built-in rule** (§5) is exactly the block shown above, fields in the order shown. Its
`rule_id` is:

```
7dc618e436c3c56405e6de47fad9608840c2adad6689b1a115476c1e02674870
```

(Reproduce: `printf 'p2kb-delivery-filter\nformat=1\nremove_fields=documentation_level,documentation_source,enhancement_source,last_updated,manual_extraction_date,scrape_tracking,source,source_reference,sources,verified_against\nremove_column0_comments=true\n' | sha256sum`.)
Use it as a unit-test value for `RuleID`.

> **Amendment, 2026-10-10, Stephen:** one name added, `scrape_tracking`, the OBEX/Quick Bytes
> scraper bookkeeping; tracking stays in the YAML and the filter removes it. The rule block, the
> built-in rule and its `rule_id` above are the amended values (the previous `rule_id` was
> `b431af2a9f515c11fe5fd982642c636c6f8843bf89ed2c3003ee0e28c04877ee`, without the new name). The
> list is still sorted; `scrape_tracking` sits between `manual_extraction_date` and `source`. The
> server's `BuiltinRule` and its `RuleID` unit-test value change to match; a server that follows the
> index needs nothing else. The certification bundle under `cert-bundle/` is a frozen fixture of the
> earlier rule and is not rebuilt for this amendment.

## 4. The engine — format 1, exact

A **line rule, indentation-aware.** Not a YAML-aware key delete, and not a plain `grep -v`.

**Empty input produces empty output.** Otherwise, for each input line, in this order:

1. **Inside a removed field's span:** a blank line (only whitespace) is removed; a **comment-only
   line** (first non-whitespace character `#`, at any indent) is removed and does **not** end the
   span — YAML ignores comments, so the engine does too; a line whose leading-whitespace length is
   **greater** than the span's indent is removed. Any other line (at the same or shallower indent)
   **ends the span** and continues to step 2.
2. **Column-0 comment:** if `remove_column0_comments` is true and the line's first character is `#`,
   remove it.
3. **Removed field:** strip leading whitespace; if the rest starts with a name from `remove_fields`
   followed **immediately** by `:`, remove the line and open a span at its indent.
4. Otherwise keep it.

Whitespace is POSIX `[[:space:]]` = `[ \t\n\v\f\r]`. Output is every kept line followed by `"\n"`,
whether or not the input ended in one.

**Exactness details** (each is what the KB's reference engine does; the bundle tests it):
- The input is bytes, split on `\n` only. No CRLF normalization: a `\r` is just whitespace at the
  start of a line and an ordinary byte elsewhere. No Unicode handling is needed — every character the
  rule tests is ASCII.
- Indent is the **count of leading whitespace bytes**; a tab counts as 1, the same as a space.
- "Followed immediately by `:`" — `source :` (space before the colon) does not match; `sources_x:`
  does not match `sources`; `- source:` and `{source:` do not match (the first non-whitespace
  character is not part of a name).
- A field line removes the **whole line**, including any value on it (`source: "x"`).

**Why a line rule.** Some KB content uses these words as data keys, and the leading `-` or `{` keeps
them out of step 3:

```yaml
REG_ARRAY: {source: "cog registers", pointer: "register"}   # content — delivered
examples:
  - source: "CON { Motor Constants }"                        # content — delivered
```

A YAML-aware delete removes both. A plain `grep -v` removes only a block scalar's key line and leaves
its continuation lines behind: 141 `source:` values are block scalars (`source: >-`), and a
non-indentation-aware filter breaks 50 files (measured 2026-09-19).

**Why column-0 comments go as a whole class.** No keyword list to drift, and no continuation logic.
Measured 2026-10-07 at KB HEAD: 1,342 column-0 comment lines in 175 files; removing every one changes
the parsed YAML of **0** files. An indented `#` line is not touched by step 2 (it is removed only if
it falls inside a span).

**Why a comment does not end a span** (MCP review, 2026-10-07). Without it, a comment inside a
removed field ends the span early and the rest of the field ships — an escape:

```yaml
sources:
  - ledger B-112          # removed
# note                    # would end the span, then be removed as a comment
  - engineering/foo.txt   # would ship
```

Measured on the KB at the time of agreement: this changes the output of 2 files, in both cases by
also removing indented maintainer comments that sit inside a span; no content changes.

### 4.1 Reference implementation (Go)

```go
package filter

import (
    "bytes"
    "crypto/sha256"
    "encoding/hex"
    "encoding/json"
    "fmt"
    "regexp"
    "strings"
)

type Rule struct {
    Format                int
    RemoveFields          []string
    RemoveColumn0Comments bool
}

// BuiltinRule is the §3 block exactly. rule_id 7dc618e4…4870 (§3.1).
var BuiltinRule = Rule{
    Format: 1,
    RemoveFields: []string{
        "documentation_level", "documentation_source", "enhancement_source", "last_updated",
        "manual_extraction_date", "scrape_tracking", "source", "source_reference", "sources",
        "verified_against",
    },
    RemoveColumn0Comments: true,
}

const posixSpace = " \t\n\v\f\r"

var fieldNameRe = regexp.MustCompile(`^[A-Za-z0-9_]+$`)

// RefusedRule is returned when the index carries a block this engine must not apply.
// Format is the block's format when it could be read, else 0.
type RefusedRule struct {
    Format int
    Reason string
}

func (e *RefusedRule) Error() string { return "delivery_filter refused: " + e.Reason }

// ParseRule reads the index's "delivery_filter" value. Strict: every key required, exact types,
// no extra keys, no duplicate or invalid names. Anything else is a *RefusedRule (§3, §5).
func ParseRule(raw json.RawMessage) (Rule, error) {
    var head struct {
        Format *int `json:"format"`
    }
    if err := json.Unmarshal(raw, &head); err != nil || head.Format == nil {
        return Rule{}, &RefusedRule{Reason: "format missing or not an integer"}
    }
    if *head.Format != 1 {
        return Rule{}, &RefusedRule{Format: *head.Format, Reason: fmt.Sprintf("unsupported format %d", *head.Format)}
    }
    var p struct {
        Format                *int      `json:"format"`
        RemoveFields          *[]string `json:"remove_fields"`
        RemoveColumn0Comments *bool     `json:"remove_column0_comments"`
    }
    dec := json.NewDecoder(bytes.NewReader(raw))
    dec.DisallowUnknownFields()
    if err := dec.Decode(&p); err != nil {
        return Rule{}, &RefusedRule{Format: 1, Reason: err.Error()}
    }
    if p.RemoveFields == nil || p.RemoveColumn0Comments == nil {
        return Rule{}, &RefusedRule{Format: 1, Reason: "remove_fields or remove_column0_comments missing"}
    }
    r := Rule{Format: 1, RemoveFields: *p.RemoveFields, RemoveColumn0Comments: *p.RemoveColumn0Comments}
    if err := r.Validate(); err != nil {
        return Rule{}, &RefusedRule{Format: 1, Reason: err.Error()}
    }
    return r, nil
}

// Validate reports whether this engine can apply r. Format 1 only.
func (r Rule) Validate() error {
    if r.Format != 1 {
        return fmt.Errorf("unsupported format %d", r.Format)
    }
    if len(r.RemoveFields) == 0 {
        return fmt.Errorf("remove_fields is empty")
    }
    seen := map[string]bool{}
    for _, f := range r.RemoveFields {
        if !fieldNameRe.MatchString(f) {
            return fmt.Errorf("field %q is not a literal key name", f)
        }
        if seen[f] {
            return fmt.Errorf("field %q listed twice", f)
        }
        seen[f] = true
    }
    return nil
}

// RuleID is §3.1: SHA-256 of the canonical text, lowercase hex.
func (r Rule) RuleID() string {
    text := fmt.Sprintf("p2kb-delivery-filter\nformat=%d\nremove_fields=%s\nremove_column0_comments=%t\n",
        r.Format, strings.Join(r.RemoveFields, ","), r.RemoveColumn0Comments)
    sum := sha256.Sum256([]byte(text))
    return hex.EncodeToString(sum[:])
}

func leadWS(s string) int { return len(s) - len(strings.TrimLeft(s, posixSpace)) }

// Apply removes provenance from one raw YAML file. Hash the raw body BEFORE calling this.
func Apply(r Rule, content string) string {
    if content == "" {
        return ""
    }
    fields := make(map[string]bool, len(r.RemoveFields))
    for _, f := range r.RemoveFields {
        fields[f] = true
    }
    lines := strings.Split(content, "\n")
    if strings.HasSuffix(content, "\n") {
        lines = lines[:len(lines)-1]
    }
    var b strings.Builder
    dropping, dropIndent := false, 0
    for _, line := range lines {
        if dropping {
            trimmed := strings.TrimLeft(line, posixSpace)
            if trimmed == "" || strings.HasPrefix(trimmed, "#") {
                continue // blank or comment-only: removed, span continues
            }
            if leadWS(line) > dropIndent {
                continue
            }
            dropping = false // span ended; this line is still tested below
        }
        if r.RemoveColumn0Comments && strings.HasPrefix(line, "#") {
            continue
        }
        ind := leadWS(line)
        rest := line[ind:]
        if i := strings.IndexByte(rest, ':'); i > 0 && fields[rest[:i]] {
            dropIndent, dropping = ind, true
            continue
        }
        b.WriteString(line)
        b.WriteString("\n")
    }
    return b.String()
}
```

The KB's reference engine is `filter_metadata()` in `engineering/tools/p2kb/fetch-kb-file.sh`; the
certification bundle's expected outputs are produced by running it (§9), not by hand. The Go text
above is not compiled on the KB side (no Go toolchain here) — the bundle is the proof. It
**replaces** the server's current five-field `FilterMetadata` regex entirely; nothing of the old
filter remains.

## 5. Determining the rule in effect

Run this **at startup** (against the cached index, if there is one) and **after every index load or
refresh**:

1. The index has a `delivery_filter` block and `ParseRule` accepts it → **that rule**, source
   `index`. Persist it as the **last-good rule** (a small file next to the cached index).
2. Otherwise — no block, or a block `ParseRule` refuses — → the **last-good rule** if one is
   persisted, source `last-good`; if none, **`BuiltinRule`**, source `built-in`.

Never apply a refused block, and never drop from a known rule to something weaker. A
missing block and a refused block are treated alike so that neither can make the server filter
less than it last did. (Before the first KB release that carries a block, every server runs on
`BuiltinRule`.)

Report the outcome in `p2kb_version` (§7). This is a maintainer diagnostic; the consuming agent is
not expected to act on it — a filter failure gives it extra provenance lines beside content that is
still correct.

### 5.1 Where the filter applies

**Every file the server fetches from under `deliverables/ai/P2/` is filtered immediately after its
hash check, before it is parsed, cached or returned** — the bodies `p2kb_get` returns, and equally
the OBEX object YAMLs (`deliverables/ai/P2/community/obex/objects/*.yaml`, which are KB files listed
in the main index) that the `p2kb_obex_*` tools read. No path uses a raw body. (Measured 2026-10-07:
the OBEX objects carried none of the §3 fields and one column-0 comment, in `_template.yaml`. Since
the 2026-10-10 amendment they carry `scrape_tracking:`, which the filter removes, so the `p2kb_obex_*`
tools no longer see the scraper bookkeeping — see the amendment note below §3.)

## 6. Cache

- **Hash before you filter** — unchanged: SHA-256 of the raw HTTP response bytes (the committed git
  blob bytes, exactly as served), compared with the index entry's `sha256`, **then** filter. A
  mismatch is a stale/poisoned body → re-fetch.
- **Cache only filtered bodies**, each filtered under the rule in effect.
- **Cache stamp = `rule_id` + `"/"` + the server's engine version** (an engine version string you
  bump whenever `Apply` or `ParseRule` changes). Store it with the cache. Every time §5 determines
  the rule in effect — **at startup and after every index load or refresh** — compare the stamp:
  different → discard every cached body and write the new stamp. **A cache with no stamp is
  discarded** — that clears old `sources:` blocks for installs upgrading from a server version that
  predates this agreement. This covers a rule change, an engine change and an upgrade, with no manual
  flush.
- Per-entry `mtime` / `sha256` invalidation is unchanged.

## 7. `p2kb_version` additions (diagnostic)

Add these fields (names as given, so the KB's acceptance probe can read them):

| Field | Value |
|---|---|
| `filter_rule_id` | `rule_id` of the rule in effect |
| `filter_rule_source` | `index` \| `last-good` \| `built-in` |
| `filter_engine_version` | the engine version in the cache stamp |
| `filter_rule_refused` | present only when the index's block was refused: `{ "format": <int or 0>, "reason": "<RefusedRule.Reason>" }` |

## 8. What the KB guarantees

1. Every KB release index carries `delivery_filter`.
2. The rule changes **only** in a KB release, never between releases.
3. At every release, the KB applies the published rule with its reference engine to every file and
   **fails the release** if: the output deletes anything YAML reads as content (over-removal); the
   output contains a provenance marker — a bench-ledger / finding id, a repo path, a `file:line`
   citation (escape); or the KB's own scripts cannot read the rule back out of the generated index.
4. The KB prefers putting provenance in the existing keys over growing `remove_fields` (Stephen,
   2026-10-04, F-545). A new name is added only in a KB release, after the over-removal check passes.

## 9. Certification — before either side releases

Neither side releases until the server matches the KB's reference output on every file. Nothing is
pushed; we iterate locally until both agree.

### 9.1 The bundle

The KB builds a self-contained bundle from the **committed** YAMLs at a recorded HEAD (so the index,
including `mtime` and `sha256`, is exactly what a release would publish). Stephen copies it into the
MCP environment.

```
p2kb-filter-cert/
├── README.md                 # KB commit, rule_id per rule, file count, how to run
├── MANIFEST.sha256           # sha256 of every file below — check the copy first
├── serve/                    # the P2KB_BASE_URL root; mirrors the raw.githubusercontent paths
│   ├── deliverables/ai/p2kb-index.json
│   ├── deliverables/ai/p2kb-index.json.gz
│   └── deliverables/ai/P2/**.yaml          # raw, unfiltered (the server fetches nothing else)
├── expected/<index key>.yaml # the KB reference engine's output, one per index entry
├── variants/
│   ├── A-unknown-format/p2kb-index.json.gz        # delivery_filter.format = 2
│   └── B-changed-fields/p2kb-index.json.gz        # a different remove_fields list
│       └── expected/<index key>.yaml              # reference output under rule B
└── vectors/input.yaml, vectors/expected.yaml      # golden edge cases, format 1
    vectors/empty-input.yaml, vectors/empty-expected.yaml   # zero bytes in, zero bytes out
```

`vectors/input.yaml` covers, among the existing edges, a comment-only line (column 0 and indented)
inside a removed field's span followed by more of that field's lines — all removed.

### 9.2 Running it

**`P2KB_BASE_URL`** (implemented by the server in this work; listed in the spec but not implemented
today) replaces the prefix `https://raw.githubusercontent.com/ironsheep/P2-Knowledge-Base/main`. The
index is fetched from `<base>/deliverables/ai/p2kb-index.json.gz`; each file from
`<base>/<files[key].path>`. No trailing slash on `<base>`. `serve/` is laid out to match.

Serve `serve/` with any static HTTP server (e.g. `python3 -m http.server 8080 -d serve`), set
`P2KB_BASE_URL=http://localhost:8080`, start from an **empty cache directory**, and run the steps
**in order**. "Fresh cache" below means: stop the server, delete the whole cache directory —
including the stamp and the last-good rule file — and start again.

1. **Golden vectors** (unit test, no server): with `BuiltinRule`,
   `Apply(vectors/input.yaml) == vectors/expected.yaml` and
   `Apply(vectors/empty-input.yaml) == vectors/empty-expected.yaml` (both zero bytes), byte for byte.
   `BuiltinRule.RuleID()` equals the value in §3.1.
2. **Whole KB:** for every key in the index, the **`content` field** of the `p2kb_get` result ==
   `expected/<key>.yaml`, byte for byte (the tool returns JSON with the YAML in that field). This
   applies to every output comparison below. `p2kb_version`: `filter_rule_source` = `index`,
   `filter_rule_id` = the README's main `rule_id`.
3. **Variant A (refused block):** replace the served `p2kb-index.json.gz` with A's; `p2kb_refresh`.
   `p2kb_version`: source `last-good`, same `rule_id` as step 2, `filter_rule_refused.format` = 2.
   Outputs still equal `expected/`.
4. **Variant B (changed rule):** replace it with B's; `p2kb_refresh`. `p2kb_version`: source
   `index`, B's `rule_id` (README). Outputs equal `variants/B-changed-fields/expected/` — which can
   only happen if the bodies cached under the main rule were discarded.
5. **No rule block:** serve the main index with `delivery_filter` removed (the README gives the
   command); **fresh cache**. `p2kb_version`: source `built-in`, `rule_id` = §3.1's built-in value.
   Outputs equal `expected/` (the main rule and the built-in rule are identical).
6. **Unstamped cache (upgrade path):** with the main index served, populate a cache, then stop the
   server and delete **only** the cache stamp; start again. Every cached body is discarded and
   re-fetched; outputs equal `expected/`.
7. **Restart keeps a valid cache:** stop and start with the stamp intact; no body is re-fetched
   (from your logs) and outputs equal `expected/`.

The variants' `files` entries and `sha256` values are identical to the main index — only the rule
differs. Also unit-test `ParseRule` on: a missing `remove_column0_comments`, a string `format`, an
extra key, a duplicate field name, an empty list, a name with a `-` — each must be refused.

### 9.3 Reporting back

Send Stephen: the server version tested, pass/fail per step, and every mismatching key with a diff.
A mismatch is a finding about one of the two engines — we decide which together, and the side at
fault fixes it; the KB rebuilds the bundle if its engine or rule changed.

## 10. Release and acceptance

1. **KB releases first.** Its index carries the rule; servers built before this change ignore the
   new key, so the KB release is harmless to them.
2. **Server releases** against that index — when Stephen says; not before the KB release is live.
3. **Live acceptance** (the KB runs it after `p2kb_refresh`):

```
p2kb_version                            -> filter_rule_source "index";
                                           filter_rule_id = the KB release's rule_id
p2kb_get p2kbSpin2Pinstart              -> no "sources:" key; the description still contains
                                           "SYNCHRONOUS serial transmit (%11100) is the opposite"
p2kb_get p2kbPasm2InstructionSkipping   -> no line starting "#"; "pattern_consumption"
                                           still lists the AUGS rule
p2kb_get p2kbHwAddonMotorDriverAddonMotorDriver
                                        -> no "source:" blocks, no "engineering/ingestion" text
p2kb_get p2kbSpin2DbgDebugFormattersArrays
                                        -> REG_ARRAY still reads {source: "cog registers", ...}
p2kb_get p2kbHwEdgeStandardModuleEdgeStandardModule
                                        -> boot_pin_direction_note still contains
                                           "boot sources: flash SPI CLK on P60"
```

The last two prove nothing was over-removed. Report the live server version; the KB closes F-439
and records it.

## 11. Review questions — answered by the MCP agent, 2026-10-07

1. **`P2KB_BASE_URL`** — not implemented today although the spec lists it; the server implements it
   for the index and content fetches in this work. The server never fetches `manifests/`, so the
   bundle carries none (§9.1).
2. **Persisting the last-good rule (§5)** — agreed: a small file next to the cached index.
3. **The `rule_id` text (§3.1)** — kept as proposed.
4. **Bundle needs** — the two new vectors (§9.1) and comparison on the `content` field (§9.2).

The MCP agent also confirmed one known limit as acceptable: a block-scalar content line that begins
with a removed field name (the F-544 case) is still removed by step 3, and §8.3's over-removal gate
fails the KB release on it.

## 12. Server implementation checklist

Everything the server must do, each pointing at its section:

- [ ] Delete the old five-field `FilterMetadata`; add `Rule`, `BuiltinRule`, `ParseRule`,
      `Validate`, `RuleID`, `Apply` exactly as §4.1 (§3, §3.1, §4).
- [ ] Read `delivery_filter` from the index (`json.RawMessage`; absent is normal) on every index load
      and refresh (§3).
- [ ] Determine the rule in effect at startup and after every index load/refresh: index → last-good →
      built-in; persist last-good; never apply a refused block (§5).
- [ ] Filter every file fetched from `deliverables/ai/P2/`, OBEX object YAMLs included, before it
      is parsed, cached or returned; no raw path (§5.1).
- [ ] Hash the raw body against `sha256`, then filter, then cache (§6).
- [ ] Cache stamp `rule_id/engine-version`: checked at startup and after every index load/refresh;
      discard on mismatch or absence; bump the engine version whenever `Apply`/`ParseRule` change
      (§6).
- [ ] `p2kb_version`: `filter_rule_id`, `filter_rule_source`, `filter_engine_version`,
      `filter_rule_refused` (§7).
- [ ] Implement `P2KB_BASE_URL` for the index and file fetches (§9.2).
- [ ] Unit tests: golden vectors, empty input, `RuleID` value, the six `ParseRule` refusals (§9.2).
- [ ] Certification steps 1–7 against the bundle, reported per §9.3.
- [ ] Release only after the KB release is live, when Stephen says (§10).

**Where this agreement and `P2KB-MCP-SPECIFICATION.md` differ, this agreement wins.** The spec was
rewritten 2026-10-07 to the current interface and points here for everything filter-related.

**The bundle** is built by the KB after its side is certified; Stephen copies it to you. Its
`README.md` carries the KB commit, every `rule_id`, the file count, and the command for step 5.

---

*Companion: `P2KB-MCP-SPECIFICATION.md` — the interface as it stands (rewritten 2026-10-07; the
original 2025 design is that file at commit `804715b7`).*
