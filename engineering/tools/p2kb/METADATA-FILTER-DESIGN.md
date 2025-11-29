# Metadata Filter Design v3.0

## Purpose

Filter non-essential metadata fields from YAML content on download to reduce token overhead.
Estimated savings: ~37,748 tokens across full knowledge base.

## Fields to Filter

These fields provide editorial/tracking metadata but not technical content:

- `last_updated` - Editorial timestamp
- `enhancement_source` - Where enhancement came from
- `documentation_source` - Original doc reference
- `documentation_level` - Completeness rating

## Filter Pattern

Key-specific regex matching only YAML keys at line start:

```bash
grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level):"
```

### Why This Pattern

- `^[[:space:]]*` - Match line start with optional indentation
- `(field1|field2|...)` - Match specific field names
- `:` - Require colon (YAML key syntax)
- `-v` - Invert match (exclude matching lines)
- `-E` - Extended regex for alternation

### Safety

This pattern avoids false matches when these strings appear in content values:
- Only matches at line start (key position)
- Requires trailing colon (key syntax)
- Won't match `description: "See documentation_source for details"`

## Implementation

**Option A (Selected): Filter on Download**

Source YAML files remain unchanged. Filtering happens at consumption time in fetch scripts.

Benefits:
- Source files retain full metadata for editorial use
- No risk of data loss
- Easy to adjust filter without regenerating content

## Usage in Fetch Scripts

### Bash
```bash
curl -sS "$url" | grep -v -E "^[[:space:]]*(last_updated|enhancement_source|documentation_source|documentation_level):"
```

### PowerShell
```powershell
(Invoke-WebRequest -Uri $url).Content -split "`n" |
  Where-Object { $_ -notmatch '^\s*(last_updated|enhancement_source|documentation_source|documentation_level):' } |
  Out-String
```

## Token Savings Analysis

Based on knowledge base scan:
- ~970 YAML files
- Average 4 metadata fields per file @ ~10 tokens each
- Total: ~38,800 tokens filtered
- Per-file average savings: ~40 tokens
