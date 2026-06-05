# Manual Layout-Standards — Sprint Plan

**Status:** Confirmed (2026-06-05)
**Effort home:** this `methodology/` folder (cross-manual effort — belongs to no single manual)
**Type:** cross-element manual-head sprint (see `.claude/skills/HEAD-DISPATCH-DRAFT.md`)

**Source inputs (already generated — this plan builds on them, does not restate them):**
- `manual-layout-standards-INPUTS.md` + `manual-layout-standards-USER-PREFERENCES.md` — the layout **standards** (widow/orphan control, part-intro→chapter flow, keep-together, code-block page-spanning + continuation markers, concerns C1–C11).
- `manual-stylesheet-architecture-survey.md` — the **divergence/convergence** map.
- `manual-production-working-set.md` — the **scope view** (roster overlay).
- `../standards/manual-front-matter-and-code-coloring-standard.md` — settled front-matter/color standard.
- Instrument: `workspace/p2-layout-torture-test/` (29 EXPECT-box cases / 9 chapters covering C1–C11).

---

## Goal

A correct, repeatable manuscript layout (no orphaned titles, clean page splits,
accurate continuation headers) across the live manuals — proven first on the
torture-test instrument, then migrated manual-by-manual with visual proof at
each step.

## Architecture reality: standalone stacks, near-identical by lineage

Each manual's stylesheets are **standalone** (its own copy — no shared include).
They are near-identical only because the platform was copied and lightly forked.
The survey's similarity tiers therefore predict **how clean each migration copy
will be**, not a shared-file edit:

| Tier | Manuals | Similarity to standard | Migration cost |
|------|---------|------------------------|----------------|
| **1 — twins** | iosp, assembly (pasm2), debug-window, streamer | **98.9%** | near-verbatim copy of the proven stylesheet |
| **2 — light fork** | pasm-desilva | 78.6% | careful port (preserve pedagogical styling) |
| **2 — moderate fork** | single-step-debugger (ssdbg) | 60.4% (40% unique) | careful merge |

**AI Privacy Guide is isolated by construction.** Because every stack is
standalone, changing a manual's stylesheets cannot touch AI Privacy — it has its
own (pristine) stack and is **automatically unaffected. No action, no
verification step needed.**

## Scope

- **In scope:** the **6 live manuals** — migrate the proven stylesheet into each standalone stack and visually prove each.
- **Instrument:** P2 Layout Torture Test — the proving ground (Phase 1), not a deliverable.
- **Automatically out (standalone, untouched):** AI Privacy Guide.
- **Out of scope:** Spin2 Reference (parked), Green Book (orphaned) — reconcile only if revived/promoted.

## Entry baseline

The 6 current generated PDFs (sizes/dates captured 2026-06-04 in `manual-production-working-set.md`)
are the pre-change reference. Exit = re-rendered, visually correct against the standards, no regressions.

---

## Confirmed decisions

1. **AI Privacy** — isolated by construction (standalone stack); untouched, no verify step.
2. **Sweep order** — **Streamer first** (most important to the community), then the rest **smallest → largest by PDF-generation time** (the largest run is ~25 min — do it last, not first). Proxy order by captured PDF size: **streamer → single-step → desilva → debug-window → io-smart-pins → assembly**. (deSilva and ssdbg are the fork merges; their small size lets us iterate them fast even though the port is careful.)
3. **Common locus** — develop/prove the standard stylesheet on the torture test, then **migrate (copy/rebase) it into each manual's standalone stack** — formalizing the existing hand "rebase on the iosp standard" practice.
4. **Plan/effort home** — this `methodology/` folder.

---

## Phases

### Phase 1 — Prove the instrument, lock the standard stylesheet against it

1. Confirm the torture test exercises **every** documented concern (C1–C11) — the instrument is itself correct/complete.
2. Iterate the **standard stylesheet** until the torture-test PDF renders correct against `manual-layout-standards-INPUTS.md` / `-USER-PREFERENCES.md`.
3. **DONE when:** the torture-test PDF is visually clean against the standards; that stylesheet is the canonical source migrated into each manual.

*(Verification each render = `document-finalize` + its overlay: gather every layout defect with chapter+location, fix the batch, render once.)*

### Phase 2 — Sweep the live manuals one by one (migrate + visually prove)

For each manual in the confirmed order (**streamer first**, then small→large):
1. Migrate (copy/rebase) the proven stylesheet into the manual's standalone stack.
2. Regenerate the PDF (Forge).
3. **Visually prove** via a `document-finalize` pass (located verify-list, batch).
4. If the manual surfaces a layout case the torture test didn't cover → **feedback loop:** add the case to the torture test, update the standard stylesheet, re-prove the instrument (Phase 1), then continue. ("Update the stylesheets if we need to.")
5. Flip that manual's roster **convention-reconciled?** to `yes`.

## Definition of done

- Standard stylesheet locked + proven on the torture test.
- All 6 live manuals migrated and visually proven; roster `convention-reconciled?` flipped to **yes** for the 4 pending, the 3 originals re-verified.
- Torture test + standard stylesheet stand as the maintained layout standard.
- AI Privacy untouched (standalone) — confirmed unaffected by construction.

## Risks / watch-items

- **assembly (pasm2)** is the largest / ~25-min generation — sequenced last so we don't burn the slow loop early.
- **ssdbg** (40% unique) and **deSilva** (pedagogical styling) are careful merges, not verbatim copies — verify their voice/structure survives the rebase.
- Feedback-loop discipline: a manual-discovered case goes back through the **instrument**, so the standard stays single-sourced (don't hand-patch one manual and skip the torture test).
