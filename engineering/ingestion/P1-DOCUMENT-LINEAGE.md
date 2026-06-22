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
| P1 Propeller Manual v1.1 Supp/Errata | **v1.1→v1.2 changelog** (NOT a layer over v1.2) | ⚠️ Corrects the charter §1 assumption: this doc *tracks the changes that produced v1.2 from v1.1* (verified from its own header). v1.2 **already incorporates** all of it — so it does NOT supersede our v1.2 corpus. Ingested 2026-06-22 as a **QA checklist** (all ~35 items confirmed present in the v1.2 extraction, 0 defects) + v1.1→v1.2 provenance. No `F-P1-` corrections. |
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
Seeded 2026-06-22 from the P1 Propeller Manual v1.2 (Ch1). P1 side is source-cited (`complete-architecture-hardware.md`);
P2-side figures to confirm against `deliverables/ai/P2/` are flagged. The full footnoted comparison lives in
`central-analysis/p1-p2-comparison/P1-P2-FEATURE-COMPARISON.md` (these edges are the manual-sourced subset feeding it).
| P1 fact / area | P2 analog | Relationship |
|----------------|-----------|--------------|
| 8 cogs, Cog RAM 512×32 longs each (p22) | 8 cogs, 512-long register RAM + 512-long LUT RAM each | **same count, P2 adds LUT RAM** |
| Hub round-robin, hub+bus at ½ sysclock, slot every 16 sysclocks; hub ops 8–23 cycles (p24) | "egg-beater" hub, per-cog slice timing | **changed** (mechanism + timing) |
| 32 I/O pins (Port A), wired-OR cog collective (p26) | 64 smart-pin I/O | **expanded + changed** (smart pins vs wired-OR) |
| INB/OUTB/DIRB "reserved for future use", no Port B (Table 1-3) | 64 pins realized via P2's pin scheme | **new-in-P2** (P1's reserved Port B never shipped) |
| 2 Counter modules + PLL per cog: CTRA/CTRB, FRQA/B, PHSA/B (Table 1-3) | smart pins (counter modes moved to pins) | **removed/replaced** |
| Video Generator per cog: VCFG/VSCL (Table 1-3) | streamer + smart pins | **changed** |
| No interrupts ("Propeller has no need for interrupts", p13) | interrupts + event system | **new-in-P2** |
| 8 lock bits (semaphores) in Hub (p30) | 16 locks | **same concept, count changed** (confirm 16 vs P2KB) |
| System Counter: global RO 32-bit CNT (p27) | CNT counter | **same concept** |
| Main Memory 64 KB = 32 KB RAM + 32 KB ROM (p30) | 512 KB hub RAM + boot ROM | **expanded** |
| ROM log/anti-log + 2049-sample sine table (p34) | CORDIC solver (QSIN/QLOG/QEXP etc.) | **new-in-P2** (hardware math replaces ROM tables) |
| Clock: CLK register, RCFAST ~12 MHz / RCSLOW ~20 kHz / XTAL+PLL ×1–16, 64–128 MHz PLL (p28–29) | HUBSET clock config, different PLL/range | **changed** |
| Boot: Cog 0 Boot Loader from ROM; P30/P31 host serial, P28/P29 I²C EEPROM 24LC256 (p18) | boot ROM; different pins/protocol + flash boot | **changed** |
| Spin (interpreted from ROM) + PASM1 (p18) | Spin2 (interpreted) + PASM2 (different encoding) | **evolved** |
