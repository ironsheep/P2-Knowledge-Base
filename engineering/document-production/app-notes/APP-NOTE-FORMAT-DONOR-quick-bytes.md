# App-Note Format Donor — Quick Bytes

> **Status:** v1 (2026-06-29), *Capability Coverage & App-Note Roster* sprint,
> Phase 3b (task #133). Quick Bytes are the **format/structure pattern donor**
> for the P2 app-note doc class (the P1 app notes are the *voice/depth* donor —
> see `P1-DOCUMENT-LINEAGE` / `APP-NOTE-VOICE-GUIDE.md`). This profile is the
> structural input the `APP-NOTE-CREATION-GUIDE.md` consumes. Derived from the
> 42 Quick Byte pages cataloged in Phase 3a (raw HTML preserved during that
> scrape). Decision context: `APP-NOTE-DESIGN-DECISIONS.md` (Decision 1).

## The consistent Quick Byte page skeleton

All 42 Quick Byte pages share one section structure (conditional sections in
brackets — present only when the task needs them):

1. **Description** — *what this does + why you'd want it* (the task framing).
2. **Demo video** — embedded near the top; *see it work* (YouTube).
3. **[Connect Up Your Hardware]** — wiring / setup (when there's hardware).
4. **[Load the Code]** — how to build/run it.
5. **Parts Used** — the bill of materials (prerequisites).
6. **Source Code** — the downloadable, runnable artifact (the center of gravity).
7. **Programming Language** — Spin2 / PASM2.
8. **Tools and Operating System** — toolchain / environment prerequisites.
9. **Additional Resources** — datasheets, related links (reference *out*, not reproduced).
10. **Document Author** / **Source Code Author** — provenance.

## Keep vs. discard (pedagogical structure vs. marketing chrome)

Per Decision 1's critical-filter rule: adopt the pedagogically-motivated
structure, discard the marketing/board-CTA structure. Don't cargo-cult.

| Quick Byte element | Verdict | Why |
|---|---|---|
| Description (task framing + why-you'd-want-it) | **KEEP** | Task-framing, not subsystem-framing — the right opening for an app note. |
| Demo video | **KEEP** (as a modality link) | "See it work" lowers the entry barrier; link it, the app note doesn't host it. |
| Connect Up Your Hardware | **KEEP** | Concrete setup the reader needs before code. |
| Load the Code | **KEEP** | How-to-run keeps it actionable. |
| Parts Used (BOM) | **KEEP** (concept) | Prerequisites belong up front. *Discard* the store/affiliate "buy now" framing — list the part, not the cart link. |
| Source Code (runnable artifact) | **KEEP — the anchor** | A validated, runnable artifact at the center is the single most important inheritance. |
| Programming Language / Tools & OS | **KEEP** (as metadata) | Environment prerequisites; terse. |
| Additional Resources | **KEEP** | Reference-out (datasheets, related objects) instead of bloating the doc. |
| Document / Source Code Author | **KEEP** (provenance) | Attribution belongs in the trust chain. |
| Site nav, newsletter signup, social icons, related-products, board-purchase CTAs | **DISCARD** | Marketing chrome — not content structure. |

## The telling absence — where Quick Bytes stop and app notes begin

The Quick Byte skeleton has **no "How It Works" / "Why this approach" / "Gotchas"
section.** Quick Bytes go *Description → wire → load → done*. There is no
composition reasoning, no engineering rationale, no edge-cases/troubleshooting,
no design tradeoffs. That is exactly the depth a Quick Byte trades away (and
what the P1 app notes provided) — and therefore exactly what our app notes must
**add**, not duplicate.

## The resulting app-note structure (fuse, don't clone)

Graft the app-note *depth* into the middle of the Quick Byte *ergonomic front*:

```
[ Quick-Byte ergonomic front ]
  1. Task statement (what + why you'd want it)        ← QB Description
  2. Modality links: demo video, OBEX object(s)       ← QB video + cross-links
  3. Prerequisites: parts, wiring, tools/environment  ← QB Parts/Connect/Tools

[ App-note depth — THE ADDED VALUE (no QB analogue) ]
  4. How it works — the composition: which subsystems, wired how, and WHY
  5. The worked, validated code (the anchor)          ← QB Source Code, but ours + pnut_ts-checked
  6. Gotchas / edge cases / tradeoffs

[ Close ]
  7. Additional resources (reference out)             ← QB Additional Resources
  8. Provenance / attribution                         ← QB Document/Source-Code Author
```

This realizes Decision 1's principle (*[QB front] → [app-note body]*) as a
concrete section order. The front is scannable and lowers the entry barrier; the
body delivers the *why* and the composition that an agent and a serious engineer
need. The runnable code stays central — but it is **ours, validated**, with the
companion YAML carrying its structured digest (Decision 2).

> Consumed by `APP-NOTE-CREATION-GUIDE.md` (the doc class). Pairs with the
> P1-sourced `APP-NOTE-VOICE-GUIDE.md` (voice/depth donor).
