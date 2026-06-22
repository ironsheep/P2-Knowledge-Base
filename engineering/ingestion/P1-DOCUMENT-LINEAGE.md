# P1 — Document Lineage (Derivation & Supersession)

> P1 editions/supersession + source→output lineage + the **P1↔P2 cross-corpus edges**. Standalone, parallel to
> the P2 `DOCUMENT-LINEAGE.md`. Stood up 2026-06-22 (P1 bootstrap). The lineage half of the P1 trust chain.

## Trust chain
Golden Parallax P1 docs → qualified (per `P1-AUTHORITATIVE-SOURCES`) → **P1 YAML KB** (`deliverables/ai/P1/`) →
agents writing P1 code + P1→P2 migration guides.

## Editions & supersession
| Source | Relationship | Note |
|--------|--------------|------|
| P1 Propeller Manual v1.2 | base | the architecture/language spine |
| P1 Propeller Manual v1.1 Supp/Errata | **correction layer over** v1.2 | errata wins on corrected points (authority order) |
| P1 Datasheet v1.4.0 | base | hardware/electrical |
| XBee Tutorial errata v1.0 | correction layer over | XBee Tutorial v1.0.1 |
| (prior P1 manual extraction, text-only) | superseded by | the backbone re-extraction (§0.6 re-extraction — archive prior) |

## Source → output lineage  ‹which inputs feed which produced output›
| Produced output | Primary sources | Cross-check |
|-----------------|-----------------|-------------|
| `deliverables/ai/P1/language/spin1/` | P1 Propeller Manual (+errata) | deSilva tutorial; app notes |
| `deliverables/ai/P1/language/pasm1/` | P1 Propeller Manual (+errata) | datasheet |
| `deliverables/ai/P1/architecture/` | P1 Propeller Manual · P1 Datasheet | — |
| `deliverables/ai/P1/hardware/` | P1 Datasheet v1.4 · Manual | — |
| _(future)_ P1→P2 migration guide | this whole P1 corpus | `deliverables/ai/P2/` |

## P1 ↔ P2 cross-corpus edges  ‹the required pass-6 leg — how P1 facts relate to / differ from P2›
_Seeded empty; each P1 ingestion adds edges here (and into `central-analysis/p1-p2-comparison/`)._
| P1 fact / area | P2 analog | Relationship (same / changed / removed / new-in-P2) |
|----------------|-----------|------------------------------------------------------|
| _(to populate during ingestion)_ | | |
