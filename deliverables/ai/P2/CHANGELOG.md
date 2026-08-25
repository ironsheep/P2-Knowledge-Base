# P2 Knowledge Base (YAML) — release notes

**The release record for this knowledge base is the repository's
[`CHANGELOG.md`](https://github.com/ironsheep/P2-Knowledge-Base/blob/main/CHANGELOG.md).**
This file points at it and deliberately holds no entries of its own.

## Why a pointer and not a copy

That changelog's own scope note is explicit: its semver numbers *"track the knowledge base
itself — YAML data, derived JSON, download-on-demand artifacts, and ingestion tooling."* So the
YAML set already had a release record; what it lacked was a way to find it from inside the
downloaded content, which is what this file supplies.

Keeping the entries here as well would create **one fact with two homes** — and the copies drift,
because `release-yamls` writes the repository changelog and nothing writes this one. That defect
class is the reason for several of the corrections in the 1.18.0 entry, so reproducing it in the
document announcing them would be a poor joke.

## What you are looking at

Everything under `deliverables/ai/P2/` is the published knowledge base, served on demand through
the [P2 Knowledge Base MCP](https://github.com/ironsheep/P2-Knowledge-Base-MCP). The knowledge base
is always the latest release: entries are not stamped with the version that changed them, so the
changelog — not the content — is where you look to see what moved.
