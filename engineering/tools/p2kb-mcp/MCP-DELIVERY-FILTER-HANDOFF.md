# P2KB MCP — delivery filter change (handoff to the MCP agent)

**For:** the agent maintaining `P2-Knowledge-Base-MCP` (the `p2kb-mcp` server).
**From:** the P2-Knowledge-Base YAML head, 2026-10-04. Closes register finding **F-439**.
**One change:** make the server's content filter identical to the delivery filter the fetch scripts
already apply. Nothing else in the server changes.

---

## 1. Why

Every KB entry carries **provenance** — how this project knows a claim is true: `source:` /
`sources:` fields, bench-ledger ids, repo paths, line citations. Our release gates read it (it is how
an unsourced number is kept out of the KB). A code-generating agent can act on none of it, and much of
it names files that exist only inside the P2-Knowledge-Base repository. So it is removed at delivery.

The fetch scripts (`engineering/tools/p2kb/fetch-kb-file.sh` and `.ps1`) remove it. **The server does
not.** Its filter is still the original five-field line regex:

```go
// current server behaviour (P2KB-MCP-SPECIFICATION.md §Filter Implementation, now replaced)
`(?m)^\s*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):.*\n?`
```

Observed on the live server, 2026-10-04 (KB v1.23.2): `p2kb_get p2kbSpin2Pinstart` returns its
`sources:` block (a bench-ledger id and a repo path); `p2kbPasm2InstructionSkipping` returns its
`# Sources: …` comment lines. The five legacy fields are removed, so the server does filter — with the
old list.

## 2. The rule — exact, and frozen

### 2.1 What is removed

Fields (anywhere in the file, at any indent):

```
last_updated  enhancement_source  documentation_source  documentation_level  manual_extraction_date
source  sources  source_reference  verified_against
```

Comment blocks: a line starting at **column 0** with `#`, optional whitespace, then `Source`,
`Sources`, `Extracted from` or `Verified against` — plus the lines directly after it that are `#`
followed by at least one whitespace character.

**This list is frozen.** Do not add keys, and do not add "smart" handling of other key names. The KB
is responsible for putting provenance only in these keys; if the KB uses another key for provenance,
that is fixed in the KB (tracked there as F-545), never by growing this list.

### 2.2 How — a LINE rule, indentation-aware. NOT a YAML-aware strip.

The server must reproduce `filter_metadata()` in `fetch-kb-file.sh` **byte for byte**. That is an awk
program; its exact semantics are:

```awk
dropping {                                   # inside a removed field's span
    if ($0 ~ /^[[:space:]]*$/) next          # blank line: removed
    match($0, /^[[:space:]]*/)
    if (RLENGTH > drop_indent) next          # deeper than the field: removed
    dropping = 0                             # same or shallower: span ends, line continues below
}
/^#[[:space:]]*(Source|Sources|Extracted from|Verified against)/ { comment_drop = 1; next }
comment_drop {
    if ($0 ~ /^#[[:space:]]+/) next          # continuation comment: removed
    comment_drop = 0
}
/^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date|source|sources|source_reference|verified_against):/ {
    match($0, /^[[:space:]]*/); drop_indent = RLENGTH; dropping = 1; next
}
{ print }
```

Why a line rule and not a YAML parser that deletes keys by name: **some KB content uses these words as
real data keys, and the line rule keeps them** (the leading `-` or `{` means the line does not match):

```yaml
REG_ARRAY: {source: "cog registers", pointer: "register"}   # content — must be delivered
examples:
  - source: "CON { Motor Constants }"                        # content — must be delivered
    outline: "CON { Motor Constants }"
```

A YAML-aware strip would delete both. A naive non-indentation-aware line filter (`grep -v`) is also
wrong: 141 `source:` values are block scalars (`source: >-`), and dropping only the key line leaves
continuation lines that break the YAML (measured: 50 files fail to load).

### 2.3 Reference implementation (Go)

```go
package filter

import (
    "regexp"
    "strings"
)

// [ \t\n\v\f\r] is POSIX [[:space:]] (what the awk reference uses).
var (
    fieldRe       = regexp.MustCompile(`^[ \t\n\v\f\r]*(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date|source|sources|source_reference|verified_against):`)
    commentHeadRe = regexp.MustCompile(`^#[ \t\n\v\f\r]*(Source|Sources|Extracted from|Verified against)`)
    commentContRe = regexp.MustCompile(`^#[ \t\n\v\f\r]+`)
    blankRe       = regexp.MustCompile(`^[ \t\n\v\f\r]*$`)
    leadWSRe      = regexp.MustCompile(`^[ \t\n\v\f\r]*`)
)

// FilterMetadata removes provenance exactly as fetch-kb-file.sh filter_metadata() does.
// Output: every kept line followed by "\n" (awk's ORS), whether or not the input ended in one.
func FilterMetadata(content string) string {
    lines := strings.Split(content, "\n")
    if strings.HasSuffix(content, "\n") {
        lines = lines[:len(lines)-1]
    }
    var b strings.Builder
    dropping, commentDrop := false, false
    dropIndent := 0
    for _, line := range lines {
        if dropping {
            if blankRe.MatchString(line) {
                continue
            }
            if len(leadWSRe.FindString(line)) > dropIndent {
                continue
            }
            dropping = false // span ended; this line is still tested below
        }
        if commentHeadRe.MatchString(line) {
            commentDrop = true
            continue
        }
        if commentDrop {
            if commentContRe.MatchString(line) {
                continue
            }
            commentDrop = false
        }
        if fieldRe.MatchString(line) {
            dropIndent = len(leadWSRe.FindString(line))
            dropping = true
            continue
        }
        b.WriteString(line)
        b.WriteString("\n")
    }
    return b.String()
}
```

**Evidence for this algorithm (P2-Knowledge-Base side, 2026-10-04):** a statement-for-statement
Python transliteration of the code above produced output identical to the shipped shell filter on
**all 1,131 KB files plus the test-vector file (0 mismatches)**. The Go text itself was not compiled
here (no Go toolchain in this environment) — `go test` against §4.1 is the proof on your side.

## 3. What stays the same

- **Hash before you filter.** The index's `sha256` is the git-blob hash of the raw file; verify the
  raw HTTP body against it first, then filter (unchanged from the spec).
- Tool names, arguments, index handling, search — unchanged.

### 3.1 Invalidate cached bodies on deploy — required

Cached entries were filtered with the old rule. After deploying, every cached body must be re-fetched
and re-filtered (bump the cache format/version so old entries are discarded, or flush on first start).
Otherwise clients keep receiving `sources:` blocks from cache until each entry's mtime changes.

## 4. Tests

### 4.1 Golden vectors (unit) — required

In this repository: `engineering/tools/p2kb-mcp/filter-test-vectors/`

- `input.yaml` (md5 `917a8bd5e47c145a009d85cd7e8b1722`) — every edge of the rule, each line
  commented with its expected fate: column-0 provenance comment + continuations, an indented
  `# Source:` comment (kept), `source: >-` block scalar with a blank line inside its span, nested
  `source:` ended by a same-indent sibling, `sources:` list, `- source:` list item (kept),
  `source_documents:` and `sourcey:` (kept — exact names only), a deeper span under
  `verified_against:`, `#` + tab continuation, `#no-space` comment (kept), all five legacy fields, a
  field as the last line of the file.
- `expected.yaml` (md5 `33e4a2eeda5d712b1beee31bee4f66d2`) — the shipped shell filter's output for
  `input.yaml`, produced by running it, not hand-written.

`FilterMetadata(input) == expected` byte for byte.

### 4.2 Parity over the whole KB — required, once before release

Against a checkout of `P2-Knowledge-Base` at the KB release you deploy with:

```bash
sed -n '/^filter_metadata() {/,/^}/p' engineering/tools/p2kb/fetch-kb-file.sh > /tmp/filter_fn.sh
# for every path in deliverables/ai/p2kb-index.json:
bash -c 'source /tmp/filter_fn.sh; filter_metadata' < "$file" > /tmp/shell.out
# compare with FilterMetadata(contents of $file) — must be identical for all 1,131 files
```

### 4.3 Live acceptance — after the roll

```
p2kb_refresh
p2kb_get p2kbSpin2Pinstart              -> no "sources:" key; the description still contains
                                           "SYNCHRONOUS serial transmit (%11100) is the opposite"
p2kb_get p2kbPasm2InstructionSkipping   -> no line starting "# Sources:"; "pattern_consumption"
                                           still lists the AUGS rule
p2kb_get p2kbHwAddonMotorDriverAddonMotorDriver
                                        -> no "source:" blocks, no "engineering/ingestion" text
p2kb_get p2kbSpin2DbgDebugFormattersArrays
                                        -> REG_ARRAY still reads {source: "cog registers", ...}
p2kb_get p2kbHwEdgeStandardModuleEdgeStandardModule
                                        -> boot_pin_direction_note still contains
                                           "boot sources: flash SPI CLK on P60"
```

The last two prove the filter did not over-remove.

## 5. Ordering — prerequisite on the KB side

**Deploy against KB v1.23.3 or later.** v1.23.3 re-wraps two Edge-module notes whose folded prose had
a line beginning `sources:`, which this rule (correctly applied) deletes; on earlier KB versions the
server would start dropping that line exactly as the fetch scripts did (F-544). The KB release gate
now fails on any content line the filter would delete.

## 6. Report back

When it is live, tell the P2-Knowledge-Base side the server version. We will run §4.3 ourselves,
close F-439, and record the version in the register.

---

*Contract documents in this repo, updated in the same change: `P2KB-MCP-SPECIFICATION.md`
§Content Filtering (rule) and §Filter Implementation (code, now this reference implementation).*
