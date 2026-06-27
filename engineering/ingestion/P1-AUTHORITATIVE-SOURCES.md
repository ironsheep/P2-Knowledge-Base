# P1 — Authoritative Sources (Trust Catalog)

> P1 (Propeller 1) trust tiers + conflict-resolution authority order. Standalone, parallel to the P2
> `AUTHORITATIVE-SOURCES.md`. Stood up 2026-06-22 (P1 bootstrap charter §1/§2). The dashboard's Auth column
> reads tiers from here.

## Trust tiers
| Source | Tier | Origin / rationale | Edition |
|--------|------|--------------------|---------|
| P1 Propeller Manual | 🏆 | Parallax — the P1 architecture + Spin1 + PASM1 reference (P1 has **no** "Silicon Doc"; the Manual is the spine) | v1.2 |
| P1 Propeller Manual Errata | 🏆 | Parallax — **correction layer**; outranks the base Manual on points it corrects | v1.1 Supp |
| P1 Datasheet | 🏆 | Parallax — hardware/electrical authority | v1.4.0 |
| Parallax App Notes (AN001–019) | 🏆 | Parallax — applied, narrower scope. **5 ingested 2026-06-27** (wave p1-appnotes-2026-06): AN001 Counters · AN004 GUI-StartVGA · AN008 Σ∆-ADC · AN013 WMF-Menus · AN014 Coroutines; companion Spin1/PASM1 code captured into each note's `assets/code-*/` (`code_validated:false`, no P1 compiler). 12 remaining await PDFs. | per-note (2011) |
| PE Labs Fundamentals · XBee Tutorial (+errata) | 🏆 | Parallax — official tutorials | v1.2 / v1.0.1 |
| deSilva P1 Tutorial | 🟢 | community (deSilva) — pedagogical cross-check / color | — |
| Chip Gracey (designer) | 🏆 | P1 designer — tiebreaker for the unresolvable residue | — |
| flexspin | community-tier | community compiler (Eric Smith) — **compile-check only**, NOT a semantic authority; below the golden docs | 7.6.11 (pending install) |

## Authority order (conflict resolution)
```
empirical P1 hardware test (reserved; none yet)
  → P1 Propeller Manual errata (correction layer)   [golden]
  → P1 Propeller Manual v1.2                          [golden]
  → P1 Datasheet v1.4                                 [golden]
  → Parallax app notes / tutorials                    [golden, narrower]
  → flexspin compile-check  (community — confirms code BUILDS; never overrides a golden doc on semantics)
  → deSilva / community
  → (designer Chip Gracey settles the residue)
```
**Inverted vs P2:** in P2 the ratified `pnut_ts` tops the docs; in P1 the validator (`flexspin`) is community-tier
and sits *below* the golden docs — a flexspin-vs-doc disagreement resolves **doc-wins**.
