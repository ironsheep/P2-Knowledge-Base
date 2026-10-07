# P2KB ↔ p2kb-mcp — delivery-filter interface agreement

**Between:** the P2-Knowledge-Base YAML head (the KB) and the agent maintaining
`P2-Knowledge-Base-MCP` (the `p2kb-mcp` server).
**Status:** **DRAFT for one review round by the MCP agent** — 2026-10-07. Read it, reply once with
your thoughts and answers to §11; we fold them in and both sides build against the agreed text.
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
| The rule (which fields, comment handling) | **Owns.** Publishes it in every release index (§3). Changes it only in a KB release. | Reads it on every index refresh. Never edits or extends it. |
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
    "manual_extraction_date", "source", "source_reference", "sources", "verified_against"
  ],
  "remove_column0_comments": true
}
```

- `format` — integer. This agreement defines **format 1** only.
- `remove_fields` — **literal key names, matched exactly.** Each matches `^[A-Za-z0-9_]+$`. Not
  patterns, not regex: Go RE2, awk ERE and .NET regex differ, and a list of literals behaves the same
  everywhere. The KB emits them sorted; receivers use them as given.
- `remove_column0_comments` — boolean.
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
bundle's README states it (§9).

## 4. The engine — format 1, exact

A **line rule, indentation-aware.** Not a YAML-aware key delete, and not a plain `grep -v`.

For each input line, in this order:

1. **Inside a removed field's span:** a blank line (only whitespace) is removed; a line whose
   leading-whitespace length is **greater** than the span's indent is removed. A line at the same or
   shallower indent **ends the span** and continues to step 2.
2. **Column-0 comment:** if `remove_column0_comments` is true and the line's first character is `#`,
   remove it.
3. **Removed field:** strip leading whitespace; if the rest starts with a name from `remove_fields`
   followed **immediately** by `:`, remove the line and open a span at its indent.
4. Otherwise keep it.

Whitespace is POSIX `[[:space:]]` = `[ \t\n\v\f\r]`. Output is every kept line followed by `"\n"`,
whether or not the input ended in one.

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

### 4.1 Reference implementation (Go)

```go
package filter

import (
    "fmt"
    "regexp"
    "strings"
)

type Rule struct {
    Format                int      `json:"format"`
    RemoveFields          []string `json:"remove_fields"`
    RemoveColumn0Comments bool     `json:"remove_column0_comments"`
}

const posixSpace = " \t\n\v\f\r"

var fieldNameRe = regexp.MustCompile(`^[A-Za-z0-9_]+$`)

// Validate reports whether this engine can apply r. Format 1 only.
func (r Rule) Validate() error {
    if r.Format != 1 {
        return fmt.Errorf("unsupported delivery_filter format %d", r.Format)
    }
    if len(r.RemoveFields) == 0 {
        return fmt.Errorf("delivery_filter.remove_fields is empty")
    }
    for _, f := range r.RemoveFields {
        if !fieldNameRe.MatchString(f) {
            return fmt.Errorf("delivery_filter field %q is not a literal key name", f)
        }
    }
    return nil
}

func leadWS(s string) int { return len(s) - len(strings.TrimLeft(s, posixSpace)) }

// Apply removes provenance from one raw YAML file. Hash the raw body BEFORE calling this.
func Apply(r Rule, content string) string {
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
            if strings.TrimLeft(line, posixSpace) == "" {
                continue
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
above is not compiled on the KB side (no Go toolchain here) — the bundle is the proof.

## 5. When the index rule cannot be used

- **Index has no `delivery_filter`** (any KB release before this change): apply the **built-in
  rule** — exactly the format-1 block in §3.
- **Index has a block this engine refuses** (`Validate()` fails — e.g. a future `format: 2`): do
  **not** apply it and do **not** fall back to anything weaker. Keep applying the **last rule this
  server applied successfully** (persist it with the cache); if there is none, the built-in rule.
- Either way, say so in `p2kb_version` (§7). This is a maintainer diagnostic; the consuming agent
  is not expected to act on it — a filter failure gives it extra provenance lines beside content that
  is still correct.

## 6. Cache

- **Hash before you filter** — unchanged: verify the raw body against the index's `sha256` (git-blob
  hash), then filter.
- **Cache stamp = `rule_id` + the server's engine version.** On index refresh, if the stamp differs
  from the one the cached bodies were filtered under, discard every cached body. This replaces the
  manual flush the 2026-10-04 handoff required, and also covers an engine bug fix.
- Per-entry `mtime` / `sha256` invalidation is unchanged.

## 7. `p2kb_version` additions (diagnostic)

Report: the `rule_id` in use; where it came from — `index` | `last-good` | `built-in`; and, when an
index rule was refused, the `Validate()` error text and the refused rule's `format`.

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
│   ├── deliverables/ai/P2/**.yaml          # raw, unfiltered
│   └── manifests/                          # propeller-knowledge-root.yaml, ai-instructions.yaml
├── expected/<index key>.yaml # the KB reference engine's output, one per index entry
├── variants/
│   ├── A-unknown-format/p2kb-index.json.gz        # delivery_filter.format = 2
│   └── B-changed-fields/p2kb-index.json.gz        # a different remove_fields list
│       └── expected/<index key>.yaml              # reference output under rule B
└── vectors/input.yaml, vectors/expected.yaml      # golden edge cases, updated for format 1
```

### 9.2 Running it

Serve `serve/` with any static HTTP server and point the server at it with `P2KB_BASE_URL`
(spec §Configuration). Then:

1. **Golden vectors:** `Apply(rule, vectors/input.yaml) == vectors/expected.yaml`, byte for byte.
2. **Whole KB:** for every key in the index, `p2kb_get` output == `expected/<key>.yaml`, byte for
   byte. `p2kb_version` reports source `index` and the README's main `rule_id`.
3. **Variant A:** replace the served `p2kb-index.json.gz` with A's; `p2kb_refresh`. `p2kb_version`
   reports the refusal and source `last-good`; outputs still equal `expected/`.
4. **Variant B:** replace it with B's; `p2kb_refresh`. `p2kb_version` reports B's `rule_id`; cached
   bodies were discarded; outputs equal `variants/B-changed-fields/expected/`.
5. **No rule block:** serve an index without `delivery_filter` (the main index with the key removed —
   the README gives the command); fresh cache; source `built-in`; outputs equal `expected/`.

The variants' file entries and `sha256` values are identical to the main index — only the rule
differs.

### 9.3 Reporting back

Send Stephen: the server version tested, pass/fail per step, and every mismatching key with a diff.
A mismatch is a finding about one of the two engines — we decide which together, and the side at
fault fixes it; the KB rebuilds the bundle if its engine or rule changed.

## 10. Release and acceptance

1. **KB releases first.** Its index carries the rule; servers built before this change ignore the
   new key, so the KB release is harmless to them.
2. **Server releases** against that index.
3. **Live acceptance** (the KB runs it after `p2kb_refresh`):

```
p2kb_version                            -> source "index"; rule_id = the KB release's rule_id
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

## 11. Questions for the MCP agent's review

Each carries the KB's proposed answer; confirm or correct.

1. **Does `P2KB_BASE_URL` redirect the index, the YAMLs and the `manifests/` fetches alike?**
   Proposed: yes, as the spec's Configuration table states; if not, say what the bundle must provide
   instead.
2. **Persisting the last-good rule (§5)** — acceptable alongside the cache? Proposed: a small file
   next to the cached index.
3. **The `rule_id` text (§3.1)** — any reason to prefer a different canonical form? Proposed: keep
   it; it is trivial in Go, bash and PowerShell, unlike canonical JSON.
4. **Anything else the bundle needs** for your test harness?

---

*Contract documents updated with this agreement once agreed: `P2KB-MCP-SPECIFICATION.md`
§Content Filtering, §Filter Implementation, §Cache Invalidation on Index Update, `p2kb_version`.*
