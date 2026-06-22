# P1 Knowledge Base — Bootstrap Charter

**Created:** 2026-06-22 · **Status:** APPROVED — **scaffolding BUILT 2026-06-22** (Phase 1 done; backbone ingestion next) · **Scope:** one-time stand-up of the entire P1
(Propeller 1) knowledge base — PASM1 + Spin1 — spanning ~15 source ingestions.
**Sits above:** `p1-sources-ingestion-plan.md` (that is the *source inventory*; this is the *how-we-stand-up-the-corpus* layer).
**End target:** a P1 YAML KB at `deliverables/ai/P1/`, parallel to the mature `deliverables/ai/P2/`.

> **Why a charter exists.** Every P2 ingestion plugs into a *mature corpus* — a populated gap ledger, an
> authority order, trust tiers, siblings to triangulate against. **P1 starts from zero.** The cross-source /
> Q&A machinery is *corpus-relative*; bootstrapping it is a different act than adding one more document. This
> charter records the decisions and the empty-but-real scaffolding the ingestion skills need to run against P1.
> This is a **one-time** campaign — proportionate to a P1-specific charter, not a reusable "new-processor" skill.

## 1. Trust spine (SETTLED)
P1 is a mature product; its documentary sources are golden:

| Source | Tier | Role |
|--------|------|------|
| P1 Propeller Manual v1.2 | 🏆 | **primary** — architecture + Spin1 + PASM1 reference (P1 has *no* "Silicon Doc"; the Manual is the spine) |
| P1 Propeller Manual v1.1 Supp/Errata | 🏆 | **correction layer** — supersedes the base Manual on points it corrects |
| P1 Datasheet v1.4.0 | 🏆 | **primary** — hardware/electrical |
| Parallax App Notes (AN001–011…) | 🏆 | applied/narrower — official Parallax |
| PE Labs Fundamentals, XBee Tutorial (+errata) | 🏆 | official Parallax tutorials |
| deSilva P1 Tutorial | 🟢 | community cross-check / pedagogical color |
| Chip Gracey (designer) | 🏆 | tiebreaker for unresolved facts (P1 designer) |

## 2. Authority order (conflict resolution)
```
empirical P1 hardware test (reserved; none yet)
  → P1 Propeller Manual errata (correction layer)   [golden]
  → P1 Propeller Manual v1.2                          [golden]
  → P1 Datasheet v1.4                                 [golden]
  → Parallax app notes / tutorials                    [golden, narrower]
  → flexspin compile-check  (community compiler — see §3)
  → deSilva / community
  → (designer Chip Gracey settles the residue)
```
Note the **errata outranks the base Manual** on any point it corrects.

> **Key difference from P2.** In P2 the *ratified* `pnut_ts` tops the documentary sources — where the compiler
> and a doc disagree, the compiler wins. **P1 is inverted:** its validator (`flexspin`) is a **community
> compiler, less trusted than the golden Parallax docs.** So flexspin confirms code *compiles*, but where it
> would imply a semantic that contradicts the Manual/errata/datasheet, **the golden docs win.** flexspin sits
> *below* the documentary spine, not above it.

## 3. The P1 code validator — `flexspin` (DECIDED), community-tier
**Chosen:** **flexspin** (CLI-native, compiles P1+P2, no Java/GUI dependency, fleet-proven). It is the P1
analog of `pnut_ts` *mechanically*, but **not in trust:** flexspin is a **community compiler, less trusted than
`pnut_ts` and below the golden P1 docs** (§2). Its job is a **compile-check** — does the extracted code build? —
and to catch malformed extractions. It is **not** a semantic authority: a flexspin result never overrides the
Manual/errata/datasheet on what a feature *means*; a flexspin-vs-doc disagreement is a finding to resolve by §2,
usually doc-wins.

- **Install status (2026-06-22):** environment has only `pnut-ts` (P2); **no P1 compiler, no Java.** Container is
  **linux-aarch64** → need a **flexspin linux-arm64 build**. Staged (NO-COMMIT) in `REF-TOOLS-NO-COMMIT/`;
  install path = a `postCreateCommand` line that copies it from the bind-mounted dir to `~/.local/bin` (survives
  rebuilds without committing the binary — unlike the committed `pnut-ts` zip). _Awaiting the binary/source drop._
- **Degradation rule (so the campaign never blocks):** until flexspin is installed, extract + catalog P1 code
  marking each `code_validated: false (pending flexspin)`; once installed, run a one-time **validation sweep**
  over all extracted P1 code and flip the flags. The dashboard `K` cell reflects validated-vs-extracted honestly.
- **Provenance to record:** because flexspin is community-tier, every flexspin-validated example carries that the
  check was flexspin (not a ratified Parallax tool) — so trust is never overstated downstream.

## 4. Register architecture — separate P1 files, namespaced IDs (RECOMMENDED)
Keep P1 self-contained; do **not** intermix with the P2 registers:
- **IDs:** `G-P1-NNN` (gaps), `Q-P1-NNN` (expert questions), `F-P1-NNN` (corrections) — own counters, no collision with P2's `G-/Q-/F-`.
- **Files (the P1 quad + routing):**
  - `engineering/ingestion/P1-INGESTION-DASHBOARD.md` *(or a clearly-delimited P1 section of the main dashboard — TBD in §8)*
  - `engineering/ingestion/P1-AUTHORITATIVE-SOURCES.md`
  - `engineering/ingestion/P1-DOCUMENT-LINEAGE.md` (incl. the **P1↔P2 cross-corpus edges**)
  - `engineering/ingestion/P1-KNOWLEDGE-GAPS.md` (empty, with `G-P1-001` / `Q-P1-001` next-ID headers + Part B who-to-ask = Chip / P1 community)
  - P1 corrections: `F-P1-` entries (separate register or a P1 section — §8).

## 5. The pieces to build (scaffolding deliverables — empty but real)
1. **`deliverables/ai/P1/` skeleton** — mirror P2's proven structure: `language/spin1/`, `language/pasm1/`,
   `architecture/`, `hardware/` + a P1 index + the **aliases/categories findability** conventions P2 uses.
2. **The P1 quad** (§4 files), each with its headers/conventions and **0%-stub rows for all ~15 sources**.
3. **Stub source folders** for the not-yet-ingested P1 docs (per `p1-sources-ingestion-plan.md`).
4. This charter, finalized.

*(We are not inventing the skeleton — we are replicating P2's battle-tested one, empty. Low risk of wrong scaffolding.)*

## 6. Bootstrap exceptions (carve-outs the mature-corpus skills don't have)
- **Doc #1 only *raises* questions.** The first source has nothing prior to answer, so its pass-6
  "answer prior questions" leg is legitimately empty — **not** the "zero-answered = exception to justify"
  defect the `ingest-source` rule flags. This carve-out applies only to the corpus's first 1–2 docs.
- **The P1→P2 cross-corpus leg is REQUIRED.** Unlike self-contained P2, every P1 fact has a P2 analog, and the
  migration delta is a primary deliverable. So P1 pass-6 carries an extra leg: *"how does this relate to / differ
  from its P2 analog?"* → feeds `P1-DOCUMENT-LINEAGE` cross-corpus edges + the existing
  `central-analysis/p1-p2-comparison/`. (This is where a P2-applicable P1 finding gets captured + routed.)

## 7. Sequence — scaffold, backbone, then wave
1. **Scaffold** (§5) + lock §8 decisions. Serial, single bootstrap step.
2. **Backbone solo** — ingest the **P1 Propeller Manual v1.2** alone (re-extraction; fold the **errata** as its
   correction cross-check). This proves the scaffolding, seeds the gap ledger, and sets the first real trust
   tiers. Still bootstrap, not the parallel run.
3. **Wave the tail** — fan out the independent remainder (datasheet completion, ~11 app notes, PE Labs, XBee,
   deSilva) via `ingest-conductor` → `ingest-wrap-reduce` against the now-populated frame. This doubles as the
   **first real certification** of the wave skills (a 10+ document batch — exactly their purpose).

## 8. Open decisions (inputs needed to finalize)
1. **P1 compiler** — ✅ **DECIDED: flexspin** (community-tier, §3). Install pending the **linux-arm64** binary/source
   drop into `REF-TOOLS-NO-COMMIT/`; wired via `postCreateCommand` (NO-COMMIT, survives rebuilds).
2. **Dashboard placement** — ✅ **RESOLVED: standalone** `engineering/ingestion/P1-INGESTION-DASHBOARD.md` (built); the main `README.md` P1 section now points to it.
3. **Corrections routing** — ✅ **RESOLVED: separate** `engineering/operations/P1-CORRECTION-FINDINGS.md` (built, `F-P1-` IDs).
