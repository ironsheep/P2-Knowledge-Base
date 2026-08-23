# baseline-health — P2-Knowledge-Base overlay

Applies additively to the central `baseline-health` skill. Names **which
validator actually covers which tree** for the yaml:p2kb head, so "are we green"
does not read greener than it verifies.

## Augments §2a — this project's substitute gate, stated in its own terms

There is no automated behavioral test suite; the Python validators **are** §2 for
every purpose. Central §2a asks for three things in the substitute's vocabulary:

- **Failure unit** — one YAML file that fails to parse, or one unresolved
  cross-reference key, or one `validate-dod-release.py` check that reports FAILED.
- **What counts as a skip** — here a skip is *a file the validator never saw*.
  That is the whole subject of the coverage trap below, and it is why the file
  count in the output matters as much as the verdict. A gate that derives its own
  file list mechanically cannot drift this way — `verify-yaml-format.py` and the
  guide-conformance instrument both do; prefer them for that reason.
- **How to group (§4)** — by shared root cause in KB vocabulary: one renamed key
  breaking many `related:` lists, one malformed block repeated across a category,
  one index regeneration owed.

**A green substitute gate never implies the documentation is correct.** These
validators prove that the YAML parses and that its keys resolve. They cannot see
a fact that is wrong — that is `document-audit` / `document-finalize` against the
`{{DOMAIN_AUTHORITY}}`, and for anything about the silicon the real behavioral
verification lives on hardware (§2b below).

## Augments §2b — the canonical half is off-container

Per `EXEC_ENV_LIMITED` / `EXEC_ENV_CANONICAL`: the validators all run in the
container, so the YAML head's baseline is **not** provisional. Two verdicts are:
a manual's rendered PDF (Forge) and any hardware-observed P2 behavior. Never let
a green validator run stand in for either — label those provisional and name the
environment that closes them.

## Augments §2c — the per-task free checks, for THIS project

Central §2c splits audit cadence by cost and says the every-task free list is
overlay material. Here it is, and every entry is a grep or a count — no build,
no render, no board. Each hunts the same shape: **a check that reports green
because it never ran.**

| Free check | The silent-green it catches |
|---|---|
| Read the **files-checked count**, not just the verdict | The coverage trap below, in its general form. `Files checked: 0 / ALL VALID` is the canonical instance, and it looks identical to a pass. |
| Compile `debug()` code with **`pnut-ts -d`** | Without `-d` the compiler *ignores the contents of every `debug()` statement*. It exits 0. The exact "a flag that silently did not reach the compile line" shape. |
| A new YAML file → **regenerate the index before trusting crossref** | `validate-crossref-keys.py` resolves against the index, so a brand-new file reads as an unresolved target. Red here is an indexing artifact; green *before* the regen means the file was never seen. |
| A touched example `.spin2` → confirm it appears in the corpus **inventory** | `sync-manual-examples.py` and the identity gate work from a derived file list. A file the list never picked up is neither headered nor identity-checked, and nothing says so. |
| A touched guide → confirm `audit-guide-conformance.py --inventory` **names it** | The instrument globs its file set and prints its exclusions by name. A guide that landed outside the glob is ungated while the gate reads clean. |
| A new/renamed chapter in `opus-master` → confirm the assembler picks it up | A chapter absent from the assembled `.md` renders a perfectly clean PDF with the chapter missing — Forge reports 100% success. Check the assembled file, not the log. |

The block-level audit (full validators + `validate-dod-release.py`) still runs at
block boundaries per central §2c. **The manual and hardware verdicts are never
part of a block audit** — they are `EXEC_ENV_CANONICAL` and cost a round trip
through {{USER_NAME}}; §2b governs them.

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

**`BUILD_COMMAND` named the trapped script until 2026-08-15.** This overlay
documented the trap for months while the slot kept pointing at it, so anyone
following Step 0a literally got the hollow green the overlay warns about. The
slot now names `verify-yaml-format.py`. Kept here as a guardrail because the
wrong default has a live source: the filename still *reads* like the syntax gate,
and it is still the first hit for anyone grepping the tools directory.

## Caveat carried to crossref

Because `validate-crossref-keys.py` resolves against the **index**, a brand-new
content file reads as an unresolved target until the index is regenerated — so a
"red" crossref immediately after adding a file can be an indexing artifact, not a
real break. Confirm with a working-tree index regen (see the `release-yamls`
§5.5 pre-flight gate) before treating it as a regression.
