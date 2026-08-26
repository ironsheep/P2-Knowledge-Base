# The 2025 PDF-era extraction is SUPERSEDED — but deliberately NOT moved

**Superseded artifact:** `p2-documentation.txt` (247,173 bytes, 2025-08-14) and the
`part*-*.txt` slices beside it.
**Superseding artifact:** `silicon-doc-text.txt` + `complete-silicon-doc-reference.md`
(DOCX-primary, 2026-08-26).

## Why it is superseded

The prior capture is PDF-derived and carries **zero of the document's 48 tables**. It also
splits code lines: `p2-documentation.txt:208` holds `'ready to load 16 longs` with its
`SETQ #16-1` torn away onto another line, where the DOCX capture keeps the whole statement
with its tabs intact (`silicon-doc-text.txt:37`).

That damage produced at least one wrong fact that reached the shipped KB: the `$1F6`/`$1F7`
row lost the `CALLD-imm return, CALLPA parameter` wording and shipped as `CALLD-imm
parameter` — see **F-363**. The mechanism is visible in the artifact itself:
`p2-documentation.txt:907-908` are the bare token `CALLD-imm` on a line of its own, its row
shredded.

## Why it is NOT archived or moved

`ingest-source` §0.6 gates the archive-move on first redirecting downstream references, and
a move that strands a referenced path is a Sacred Rule #7 violation. Measured 2026-08-26:

| Referencing | Count |
|---|---|
| shipped KB (`deliverables/ai/P2/`) | **24** (23 with `:line` locators) |
| other `deliverables/` | 3 |
| `engineering/` working docs | 266 |
| **total** | **293** |

**So this is a mark-in-place supersession.** The file stays exactly where it is and every one
of those 293 paths keeps resolving. The physical move happens only after the references are
re-pointed, and not before.

## Status of the existing citations

Spot-checked 2026-08-26: the sampled shipped-KB locators (`:188`, `:3602`, `:3606`, `:3961`,
`:3997`, `:3999`) all resolve to content that matches what cites them. **They are not broken.**
The concern is lineage rather than correctness — they cite a capture now known to be lossy,
and that capture has produced at least one demonstrated error. Re-anchoring them to
`silicon-doc-text.txt` is tracked as **F-365**; it is hygiene work, not an emergency, and
nothing here should be read as saying those 23 citations are currently wrong.

## Prior derived artifacts in this folder

`COG-RAM-REGISTER-MAP.md`, `INSTRUCTION-TIMING-AND-ENCODING.md`, `WW-FIELD-ENCODING.md`,
`KNOWN-BUGS-CRITICAL.md`, `instruction-encodings-for-verification.md`,
`silicon-doc-v35-facts-only.md` and the `silicon-doc-v35-*` analyses were all built from the
superseded capture. They were reconciled against the new extraction in «#310»; the one
substantive disagreement found is F-363. They remain in place for lineage.
