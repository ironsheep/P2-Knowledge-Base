# P2 Knowledge Base (YAML)

The Propeller 2 knowledge base as structured YAML, optimized for AI code generation and served by the **[P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP)**.

- `architecture/` — silicon architecture (COGs, hub, CORDIC, streamer, events)
- `language/` — PASM2 instructions and the Spin2 language
- `hardware/` — boards, add-ons, and pin mappings
- `application-notes/` — worked, end-to-end techniques distilled from the published P2 application notes
- `community/` — OBEX community objects and Parallax Quick Bytes articles
- `code-examples/`, `guides/`, `tools/` — patterns, how-tos, and tooling references

## What "optimized for AI code generation" commits us to

An agent reading these files cannot weigh a hedge or push back on a wrong fact — it emits code. So this set is held to a stricter bar than prose documentation:

- **Entries cite the Parallax document that states the claim** — its title, edition and section, and the page where the document is paginated; a Parallax source listing at the edition it was read from; an OBEX object; or a test we ran: a result measured on P2 silicon, or what the compiler accepts. An entry that cannot name its authority is removed rather than shipped with a caveat.
- **A fact lives in one file**, and everything else points at that file. Duplicated text drifts.
- **Examples are meant to run exactly as written.** Every code block compiles with `pnut-ts` in the context it declares; compiling shows only that the code is legal, so what an example does is checked against its source as well.
- **Where the chip does not have a feature readers expect**, the entry says so plainly and gives the real composition that achieves the intent instead.

Cross-references between entries are written as full paths from this directory (for example `language/pasm2/wrpin.yaml`), so a reference resolves to exactly one file.

This content is machine-served; humans should start from the [repository root README](../../../README.md).
