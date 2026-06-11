# Functional-Decomposition Reasoning Layer — authoring conventions

Generative guidance that teaches a consuming agent **how to derive an object/cog
decomposition for an unfamiliar P2 hardware mix** — what P2 assets/features drive the
cuts and how to make each decision. It is the *grammar* that complements the existing
*vocabulary* (`language/spin2/concepts/object_archetypes.yaml`) and the silicon
*orientation* (`architecture/p2-architecture-mental-model.yaml`) — filling the gap
between those two altitudes (the archetypes assume the decision to create an object
was already made; the mental model stops at the silicon).

These conventions govern every entry authored under
`deliverables/ai/P2/architecture/decomposition/`. They live here in
`engineering/standards/` — not in the shipped KB tree, which carries only the YAML
knowledge base served on demand.

## Entry schema (matches the existing concept-entry style)

`concept` (snake_case id) · `title` · `category: decomposition_reasoning` · `summary`
(block) · named body sections · `related:` (list of **bare KB-root-relative file
paths**) · `see_also:` (annotated camelCase ids, `"description: p2kbKey"`) ·
`oneliner` (optional).

Force entries (resource-ownership, data-flow-contracts, rate-adaptation,
altitude-layering, cross-cutting-forces) additionally carry the five required
force-fields: `what_it_is`, `why_on_p2`, `how_it_cuts`, `example`,
`failure_if_ignored`.

## Authority-tier field (the discipline that keeps this generative)

**Every body section carries `authority_tier:`**, one of:

| Tier | Meaning | Agent freedom |
|------|---------|---------------|
| `PHYSICS` | a silicon truth that cannot be violated | none — design within it |
| `PRINCIPLE` | a force/trade-off and *why* it exists | applies it with judgment |
| `HEURISTIC` | a default **with an explicit escape condition** | overrides for a stated reason |
| `PATTERN` | one resolution of a named set of forces | consults as illustration |
| `EXAMPLE` | concrete code/derivation, frozen at one point | reads, never copies as law |

Where a section genuinely mixes tiers, **inline-tag the individual claims**. A
`HEURISTIC` with no stated escape condition is a disguised law and is a **defect**.
A `PATTERN`/`EXAMPLE` must be unmistakably marked so it can never be read as a
`PRINCIPLE`.

## Grounding (the tier selects it)

- **PHYSICS** → cite an **internal P2KB path/key** (the architectural fact). Must be
  true about the silicon.
- **PRINCIPLE / HEURISTIC / PATTERN** → cite the **durable reference canon** by full
  bibliographic identity (author, title, year). "How to decide" is not a P2 fact.
- **EXAMPLE** → **inlined, self-contained**, tagged illustrative-not-normative.

## Reference self-sufficiency (REQUIRED)

Shipped YAML is MCP-served and read standalone. It must **never** reference a
guiding/working document (the architecture-discussion inputs, the sprint/design
plans) or any relative file path to them. Absorb that substance inline. Allowed
references are self-sufficient only: (a) internal P2KB paths/keys that resolve within
`deliverables/ai/P2/`; (b) durable bibliographic citations for the canon.

## Toolchain notes

- Index key = `p2kbArch` + CamelCase(filename); the `decomposition/` subdir is **not**
  in the key unless a filename collides (e.g. `resource-ownership.yaml` →
  `p2kbArchResourceOwnership`).
- `see_also:` keys validate against the generated index, so **sibling cross-refs
  resolve only after an index regen** — full `validate-crossref-keys` over the set is
  a whole-set, post-regen gate run at release. Per-entry, keep `related:` file paths
  pointing at files that already exist.
- Register the `decomposition` category in `engineering/tools/p2kb-categories.json`
  during cross-link wiring so the area groups in the index.

## Entries (sprint plan order)

`decomposition-glossary` · `decomposition-method` · `first-contact-procedure` ·
`resource-ownership` · `data-flow-contracts` · `rate-adaptation` ·
`altitude-layering` · `cross-cutting-forces` · `spatial-computing` ·
`evaluation-vocabulary` · `resource-budget` · `worked-derivation-robot-dog`.
