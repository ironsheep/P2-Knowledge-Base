# App-Note Design Decisions

> **Status:** v1 (2026-06-29), authored under the *Capability Coverage &
> App-Note Roster* sprint (Phase 1). Records two structural decisions about what
> a P2 app note **is**, derived from the four-artifact model. These shape the
> roster framing now and the app-note authoring (and YAML-companion schema) in
> the carved-out follow-on sprint. Companions: `APP-NOTE-CREATION-GUIDE.md`,
> `APP-NOTE-VOICE-GUIDE.md`, and the standards docs
> `engineering/standards/p2-capability-taxonomy.md` +
> `.../documentation-standards/artifact-placement-rubric.md`.

---

## Decision 1 — Quick Bytes are a *format/structure pattern donor* (fuse, don't clone)

**Context.** Quick Bytes are Parallax's *deliberate replacement* of the P1
app-note format. They stopped writing P1-style long-form app notes and moved to
Quick Bytes (web page + short video + downloadable code + tags). That evolution
encodes lessons, and we re-introduce the older format for the P2 — so we should
read those lessons rather than ignore them.

**What the evolution traded:**

| Quick Bytes gained | …at the cost of (vs. app notes) |
|---|---|
| Video — *see it work* | Depth of *why* / engineering rationale |
| Web discoverability (tags, SEO) | Systematic composition reasoning |
| Brevity / approachability | Completeness, edge cases, gotchas |
| Currency + cadence | Authoritativeness / citability |
| Runnable code at the center | — |

Quick Bytes optimized for **engagement and breadth**; app notes for **depth and
authority**.

**Decision.** Our P2 app notes serve a **dual human + agent audience that needs
depth and trust** — so we **fuse Quick Byte ergonomics with app-note substance**,
we do not clone Quick Bytes.

- **Inherit from Quick Bytes:** task-framing (not subsystem-framing), a runnable
  *validated* code artifact at the center, multi-modal links (video / datasheet /
  OBEX), discoverability metadata, and brevity discipline (depth without the
  intimidating 40-page PDF).
- **Keep from app notes:** the *why*, composition reasoning, completeness, and
  trust-chain authority.
- **Resulting shape:** *[Quick-Byte-style front — crisp task statement + the
  runnable artifact + modality links] → [app-note-style body — the why, the
  composition, the gotchas].*

**Consequence — Quick Bytes is the *second* pattern donor.** The P1 app notes
are the **voice / depth** donor (profiled in `P1-DOCUMENT-LINEAGE`); Quick Bytes
are the **format / structure** donor. The app-note doc class consumes both. The
format-donor profile is harvested in this sprint (Phase 3b), **critically
filtered** to keep pedagogically-motivated structure and discard
marketing / board-CTA structure — don't cargo-cult the whole format.

**Consequence — Quick Bytes push our app notes *up* the depth axis.** Because
~42 tasks already have a "here's it working" Quick Byte, our app notes
**shouldn't duplicate that tier** — Parallax fills it. A Quick Byte *shows* a
1-Wire read; our app note teaches the *pattern and the why*. This frees the app
notes to go deeper — toward the compute-model territory (spine domain A) where
the gap analysis already points.

---

## Decision 2 — An app note is a human doc **+** a structured YAML companion

**Context.** App notes serve both humans (who read the prose) and agents (who
generate code). An agent shouldn't have to parse a PDF to use an app note's
content.

**Why app notes earn a YAML form when OBEX/Quick Bytes don't.** It's authorship.
We can only trust-stamp and serve content we *author* — community OBEX/Quick
Bytes we only *catalog* (point to). App notes are first-party and
`pnut_ts`-validated, so we can bring their content *fully* into the served KB.
App notes are the one "lesson" type an agent can consume structurally without
opening the document.

**Decision.** Each app note ships as **the human document + a structured YAML
companion** under `deliverables/ai/P2/` (first-party, trust-stampable).

**The companion is a digest + links — never a prose clone.** Two tiers:
- **Discovery tier:** task identity, capability-spine classification, summary,
  modality links. (Same shape as the OBEX/Quick Byte catalog entries.)
- **Consumption tier:** the **composition recipe** — *which KB primitives it uses,
  as links to the existing instruction/method/smart-pin YAMLs, not
  re-descriptions* — plus a reference to the runnable validated code, key
  parameters / pin-maps, prerequisites, and gotchas as structured flags.

An app note is mostly a *composition of primitives the KB already documents*.
What's novel is the composition, the task framing, the worked code, and the
*why*. The YAML carries the **novel structure + pointers to the primitives**;
the prose *why* stays in the human document. **No content lives in two places.**

**Drift control.** One authoring act emits both (the doc class gains an "emit
YAML companion" step), and an **agreement audit** checks they agree — the same
discipline as the manual↔YAML drain gate.

**Scope.** This sprint records the *principle* (it frames the roster). The
**schema + emit-mechanism is designed in the app-note authoring follow-on
sprint**, piloting on the existing **P2AN000** draft.
