# baseline-health — P2-Knowledge-Base overlay

Applies additively to the central `baseline-health` skill. Names **which
validator actually covers which tree** for the yaml:p2kb head, so "are we green"
does not read greener than it verifies.

## The coverage trap (why this overlay exists)

`validate-yaml-syntax.py` looks like the content-YAML syntax gate. It is **not**:
with `--path <dir>` it scans only `manifests/` + `engineering/knowledge-base/`
(≈4 files) and reports "Files checked: 0 / ALL VALID" for the `deliverables/ai/P2/`
content tree — a green that verifies almost nothing of what it implies.
(Observed 2026-06-11, debug-window-v55 sprint: running it on `debug-displays/`
returned 0 files checked.)

## Real coverage map for the yaml:p2kb head

When asked "are we green" for the P2KB YAML set, run and trust **these**:

| Concern | Validator that ACTUALLY covers the content tree |
|---|---|
| Content-YAML parses / syntax | `verify-yaml-format.py` (parses every `deliverables/ai/P2/` file — the true syntax gate) — or the `generate-p2kb-index.py` parse, which fails loudly on a bad file |
| Cross-references resolve | `validate-crossref-keys.py` — resolves `related:`/`combines_with:`/`related_*` against the **index** (not the filesystem); `see_also:`/`references:` are informational and always pass |
| Release readiness (index structure, gzip parity, key naming, orphans, crossref) | `validate-dod-release.py` |

`validate-yaml-syntax.py` is retained only for the `manifests/` tree it really
covers — never cite it as the content-tree syntax baseline.

## Caveat carried to crossref

Because `validate-crossref-keys.py` resolves against the **index**, a brand-new
content file reads as an unresolved target until the index is regenerated — so a
"red" crossref immediately after adding a file can be an indexing artifact, not a
real break. Confirm with a working-tree index regen (see the `release-yamls`
§5.5 pre-flight gate) before treating it as a regression.
