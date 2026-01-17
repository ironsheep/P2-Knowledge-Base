# P2KB MCP Server Update Specification: Alias Resolution

**Purpose**: This document specifies the changes needed to the P2KB MCP server to support the new alias resolution system in the p2kb-index.json.

**Date**: 2026-01-17 (Updated)
**Sprint Reference**: sprint-reference-system-fix.md
**Index Version**: 3.4.0

---

## Summary of Changes

The p2kb-index.json has been enhanced to version 3.4.0 with **array-based aliases** that enable resolution of common names (instruction mnemonics, method names, pattern IDs, symbols) to their canonical P2KB index keys.

**CRITICAL CHANGE in v3.4.0**: Aliases now return **arrays** of keys, not single strings. This ensures that when an alias like "ABS" exists in both PASM2 and Spin2, **both entries are returned** - no information loss.

---

## Index Structure Changes

### New `system` Metadata Fields

```json
{
  "system": {
    "version": "3.4.0",
    "total_aliases": 933,
    "multi_target_aliases": 54,
    // ... existing fields
  }
}
```

- `total_aliases`: Total number of alias entries
- `multi_target_aliases`: Number of aliases that map to multiple keys (54 in current index)

### New `aliases` Section (v3.4 Array Format)

The index now includes an `aliases` object that maps common identifiers to **arrays** of canonical index keys:

```json
{
  "aliases": {
    "ADD": ["p2kbPasm2Add"],
    "COGINIT": ["p2kbPasm2Coginit", "p2kbSpin2Coginit"],
    "ABS": ["p2kbPasm2Abs", "p2kbSpin2Abs"],
    "WAITMS": ["p2kbSpin2Waitms"],
    "_CLKFREQ": ["p2kbSpin2SpecialConfigurationSymbols"],
    "state_machine": ["p2kbArchStateMachineAnalysis", "p2kbSpin2Spin2StateMachine"]
  }
}
```

**Key point**: Every alias value is an array, even single-target aliases like `"WAITMS": ["p2kbSpin2Waitms"]`.

### Alias Categories

Aliases are harvested from multiple sources in YAML files:

1. **Instruction Mnemonics** (PASM2): `ADD`, `MOV`, `JMP`, etc.
2. **Method Names** (Spin2): `WAITMS`, `COGINIT`, `PINWRITE`, etc.
3. **Pattern IDs**: `motor_controller`, `state_machine`, etc.
4. **Explicit Aliases**: Values from `aliases:` field in YAML
5. **Symbol Names**: `_CLKFREQ`, `_CLKMODE`, `_XTLFREQ`, etc.

---

## Required MCP Server Changes

### 1. Load Aliases on Index Initialization

When the MCP server loads `p2kb-index.json`, it must:

```python
def load_index(self, index_path: str):
    with open(index_path) as f:
        index_data = json.load(f)

    self.entries = index_data.get("entries", {})
    self.categories = index_data.get("categories", {})
    self.aliases = index_data.get("aliases", {})  # NEW
```

### 2. Implement Alias Resolution in Key Lookup (v3.4 - Returns Array)

All key lookup operations must handle the fact that aliases return **arrays**:

```python
def resolve_keys(self, key: str) -> List[str]:
    """
    Resolve a key that might be:
    1. A canonical P2KB key (p2kbPasm2Add) -> returns [key]
    2. An alias (ADD, add) -> returns array of all matching keys
    3. An unknown key -> returns []

    v3.4: Always returns a list to preserve ALL matches.
    """
    # Direct lookup first
    if key in self.entries:
        return [key]

    # Check aliases (case-insensitive) - v3.4: aliases are arrays
    for variant in [key, key.upper(), key.lower()]:
        alias_keys = self.aliases.get(variant)
        if alias_keys:
            # Filter to only valid entries
            valid_keys = [k for k in alias_keys if k in self.entries]
            if valid_keys:
                return valid_keys

    return []
```

### 3. Update All Public API Methods to Return Multiple Results

Every MCP tool that looks up documentation must handle multiple results:

```python
def get_documentation(self, key: str) -> List[dict]:
    """
    v3.4: Returns a LIST of entries (may be multiple for aliases like ABS).
    """
    resolved_keys = self.resolve_keys(key)
    if not resolved_keys:
        return [{"error": f"Unknown key: {key}"}]

    results = []
    for canonical in resolved_keys:
        entry = self.entries[canonical].copy()
        # Add resolution metadata
        entry["_canonical_key"] = canonical
        if key != canonical:
            entry["_resolved_from"] = key
        results.append(entry)

    return results

def search_entries(self, query: str) -> list:
    # Include alias matches in search results
    results = []

    # Check if query matches an alias - get ALL targets
    for variant in [query, query.upper(), query.lower()]:
        if variant in self.aliases:
            for canonical in self.aliases[variant]:  # v3.4: iterate array
                if canonical in self.entries:
                    results.append(self.entries[canonical])

    # Continue with regular search...
```

### 4. Provide Multi-Match Information in Responses

When returning entry data, indicate if multiple matches were found:

```python
def get_documentation(self, key: str) -> dict:
    """
    Returns response with all matching entries.
    """
    resolved_keys = self.resolve_keys(key)
    if not resolved_keys:
        return {"error": f"Unknown key: {key}"}

    response = {
        "query": key,
        "match_count": len(resolved_keys),
        "entries": []
    }

    for canonical in resolved_keys:
        entry = self.entries[canonical].copy()
        entry["_canonical_key"] = canonical
        response["entries"].append(entry)

    return response
```

---

## Multi-Target Aliases (v3.4 - No Conflicts!)

**v3.4 eliminates the "first match wins" problem.** Some aliases map to multiple entries (both PASM2 and Spin2 have instructions with the same name). In v3.4, ALL matches are returned:

```json
{
  "ABS": ["p2kbPasm2Abs", "p2kbSpin2Abs"],
  "COGINIT": ["p2kbPasm2Coginit", "p2kbSpin2Coginit"]
}
```

**54 multi-target aliases** exist in the current index, including:

- `ABS`, `AKPIN`, `CALL`, `COGATN`, `COGID`, `COGINIT`, `COGSTOP`
- `GETCT`, `GETRND`, `HUBSET`, `LOCKNEW`, `LOCKREL`, `LOCKRET`, `LOCKTRY`
- `MOVBYTS`, `POLLATN`, `QEXP`, `QLOG`, `RDPIN`, `RQPIN`, `WAITATN`
- `WRPIN`, `WXPIN`, `WYPIN`
- Pattern aliases: `state_machine`, `buffer_management`, `cog_management`

**The MCP server MUST return all entries** for these aliases. Future enhancements may add context-aware prioritization (e.g., if user is asking about PASM2 code, show PASM2 entries first), but both must be included.

---

## Backward Compatibility

- **Canonical key lookup**: `get_documentation("p2kbPasm2Add")` continues to work exactly as before
- **New alias lookup**: `get_documentation("ADD")` now returns results via alias resolution
- **Array format**: All aliases are arrays (even single-target ones like `["p2kbSpin2Waitms"]`)

---

## Testing Requirements

1. **Direct Key Lookup**: `get_documentation("p2kbPasm2Add")` returns single entry
2. **Single-Target Alias**: `get_documentation("WAITMS")` resolves and returns single entry
3. **Multi-Target Alias**: `get_documentation("ABS")` returns BOTH PASM2 AND Spin2 entries
4. **Case Insensitivity**: `get_documentation("abs")` resolves same as "ABS"
5. **Unknown Key**: `get_documentation("NOTAKEY")` returns appropriate error
6. **Match Count**: Response includes count of how many entries matched

---

## Implementation Priority

1. **Phase 1**: Load aliases and implement array-based resolution (required)
2. **Phase 2**: Return all matches for multi-target aliases (required for v3.4 compliance)
3. **Phase 3**: Include resolution metadata in responses (recommended)
4. **Phase 4**: Context-aware prioritization (optional future enhancement)

---

## Files Affected

- `p2kb-index.json` - Enhanced with aliases section (already done)
- MCP server index loading code - Must parse aliases
- MCP server lookup methods - Must use resolve_key()
- MCP server response formatting - May include resolution metadata
