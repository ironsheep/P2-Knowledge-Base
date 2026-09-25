# P2 Errata — verification sidecars

One sidecar per chapter (`eN-sources.md`) maps every number, quotation and code excerpt in
that chapter to its source file and line. Each `eN-harness-*.spin2` is the compile harness for
the chapter's workaround snippet (compiled with `pnut-ts` 1.55.8; no `.bin` is kept).

**This folder is tracked on purpose.** It sits outside `audit/`, which the repo git-ignores as
working history. The sidecars are the chapters' standing proof trail.

## Reading the paths inside the sidecars

The sidecars were written 2026-09-25 while they still lived in `audit/verification/`. Their
references resolve as follows:

| Sidecar says | Where it is now | Tracked? |
|---|---|---|
| `audit/verification/eN-*` | this folder, `verification/eN-*` | yes |
| `audit/verification-tests/test-*.spin2` (the rigs) | also at `engineering/ingestion/external-sources/hardware-verification/campaigns/2026-09-p2-errata-predictions/tests/`, byte-identical (checked with `cmp` by the E1–E3 authors) | the campaign copy is |
| `audit/verification-tests/logs*/debug_*.log` (raw logs) | the local workspace only | **no**, by project rule: raw logs are regenerable from the versioned rigs, and their decisive values are carried in the ledger |
| the ledger | `engineering/ingestion/external-sources/hardware-verification/P2-EMPIRICAL-FINDINGS.md`, EF-066..070 | yes |

The rigs' internal filenames (`test-o17-…`, `test-so80-…`) are not reader names. The chapters
name the examples-archive copies instead (`e1-setq-block-pointer-step-test.spin2`, and so on),
which are the rigs with their internal header notes removed and their code unchanged.

Any mention of `/home/vscode/.local/pnut/…` in a sidecar is the brief's original compiler path,
which no longer exists; `/usr/local/bin/pnut-ts` is 1.55.8 since 2026-09-23.
