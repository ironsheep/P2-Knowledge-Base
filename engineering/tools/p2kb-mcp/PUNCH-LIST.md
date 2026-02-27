# P2KB Download-on-Demand System — Punch List

*Created: 2026-02-27*
*Last Updated: 2026-02-27*

Backlog of improvements, fixes, and audit tasks for the P2KB MCP / Download-on-Demand system and its underlying YAML knowledge base.

---

## Open Items

### PL-001: Audit All YAML Instruction Timing Against Silicon Doc

**Priority:** Medium
**Discovered:** 2026-02-27 — WAITX timing error (description said "D+1", silicon doc says "2+D"; WC/WZ/WCZ randomized delay behavior was completely missing)

**Scope:** Systematic comparison of all ~300 PASM2 instruction YAMLs against the authoritative P2 Instructions v35 CSV.

**What to check per instruction:**
- `encoding.clocks` matches CSV clock column
- `timing.cycles` matches CSV clock column
- `description` text accurately reflects the clock formula (watch for "D+1" vs "2+D" style mismatches where prose contradicts structured data)
- `oneliner` is consistent with the above
- `notes` don't contain incorrect timing claims
- Any behavioral modes (e.g., flag-dependent behavior changes) are fully documented

**Approach:** The structured fields (`encoding.clocks`, `timing.cycles`) were extracted programmatically and are likely correct. The risk is in human-readable text (`description`, `oneliner`, `notes`) where AI-generated prose may have introduced errors. Focus the audit there.

**Source:** `engineering/ingestion/sources/p2-instructions-csv/P2 Instructions v35 - Rev B_C Silicon - Sheet1.csv`

**Also tracked in:** Sprint Candidates Registry as TV-002

### PL-002: p2kb_refresh Does Not Reload Index Structure

**Priority:** High
**Discovered:** 2026-02-27 — Added new YAML, regenerated index (1027→1028 entries), called p2kb_refresh. Server returned `refreshed: true` but `total_entries` stayed 1027. New key not discoverable.

**Problem:** `p2kb_refresh` invalidates stale content caches for existing keys but does not re-parse the index file to discover new or removed keys. The in-memory index structure is only loaded once at startup.

**Expected behavior:** `p2kb_refresh` should force a full index reload from disk — re-read `p2kb-index.json`, rebuild the in-memory key map, alias map, and category map. New entries should be immediately discoverable without restarting the MCP process.

**Impact:** After publishing new YAML through the 7-step workflow, the new content is invisible to consumers until the MCP process restarts. This breaks the publish-then-use workflow within a single session.

---

## Completed Items

*(none yet)*
