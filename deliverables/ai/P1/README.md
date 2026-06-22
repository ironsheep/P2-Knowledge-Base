# P1 (Propeller 1) Knowledge Base

AI-optimized knowledge base for the **Parallax Propeller 1 (P8X32A)** — Spin1 + PASM1 — parallel to the
mature `deliverables/ai/P2/`.

> **STATUS: under construction (bootstrap, started 2026-06-22).** This tree is being stood up by the P1
> ingestion campaign. See `engineering/ingestion/plans/P1-KB-BOOTSTRAP-CHARTER.md` for the bootstrap design
> and `engineering/ingestion/P1-INGESTION-DASHBOARD.md` for source/ingestion status. Categories below mirror
> P2 conventions (aliases + categories findability, full-path cross-references).

## Layout
| Area | Holds |
|------|-------|
| `language/spin1/` | Spin1 methods, operators, constructs, built-ins |
| `language/pasm1/` | PASM1 instructions (encoding, timing, flag effects, related) |
| `architecture/` | P1 silicon architecture — cogs, hub, counters, video generator, locks |
| `hardware/` | P1 chip + board hardware (P8X32A package, pins, electrical) |

## Trust chain
Sourced via the P1 ingestion quad (`engineering/ingestion/P1-*`): golden Parallax docs (P1 Propeller Manual +
errata + datasheet) → P1 YAML here → community. Code examples are flexspin-compile-checked **when** the P1
compiler is installed (community-tier; pending — see the charter); until then they are documentary-extracted,
marked not-yet-validated.
