# P2 Knowledge Base (YAML)

The Propeller 2 knowledge base as structured YAML, optimized for AI code generation and served by the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)**.

- `architecture/` — silicon architecture (COGs, hub, CORDIC, streamer, events)
- `language/` — PASM2 instructions and the Spin2 language
- `hardware/` — boards, add-ons, and pin mappings
- `application-notes/` — worked, end-to-end techniques distilled from the published P2 application notes
- `community/` — OBEX community objects
- `code-examples/`, `guides/`, `tools/` — patterns, how-tos, and tooling references

## What "optimized for AI code generation" commits us to

An agent reading these files cannot weigh a hedge or push back on a wrong fact — it emits code. So this set is held to a stricter bar than prose documentation:

- **Entries cite the Parallax document that states the claim**, down to the page or line. An entry that cannot name its authority is removed rather than shipped with a caveat.
- **A fact lives in one file**, and everything else points at that file. Duplicated text drifts.
- **Examples are meant to run exactly as written**, and are checked for what they actually do — not merely that they compile.
- **Where the chip does not have a feature readers expect**, the entry says so plainly and gives the real composition that achieves the intent instead.

Cross-references between entries are written as full repo-absolute paths, so a citation resolves to exactly one file.

## Release record

See [`CHANGELOG.md`](CHANGELOG.md) in this directory, which points at the record of what changed and when.

This content is machine-served; humans should start from the [repository root README](../../../README.md).
