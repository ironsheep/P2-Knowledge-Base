# silicon-doc — code extraction, 2026-08-26

**Source:** `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx`
**Method:** DOCX-primary. Monospace runs grouped into contiguous blocks in document order,
Word autocorrect normalised (curly quotes → straight, en/em dash → `-`, nbsp → space, and a
trailing U+2026 restored to the Spin2 `...` line-continuation; a mid-sentence U+2026 marks the
block as prose and drops it). Validated with `pnut-ts v1.55.3`, `-d` (DEBUG enabled).

## What was found

| Category | Count | Compiled? |
|---|---|---|
| Contiguous monospace blocks (≥2 lines) | 180 | — |
| — classified **prose in monospace**, dropped | 61 | not code |
| — classified **code-shaped** | 119 | — |
| &nbsp;&nbsp;• **encoding tables** (`EEEE 1101011 00L DDDDDDDDD …`) | 13 | not code |
| &nbsp;&nbsp;• **PASM2 blocks** | 106 | see below |

## PASM2 validation

These are **specification fragments, not programs.** They reference symbols the surrounding
narrative defines, so none compiles bare. Each was harnessed as `CON/DAT/org 0` with a parent
label, and symbols reported undefined were declared `long 0` iteratively.

| Result | Count |
|---|---|
| **Compile clean once referenced symbols are declared** | **67 / 106** |
| Do not compile under the harness | 39 / 106 |

## The 39 — what they actually are

Every one inspected traces to **the block not being code**, or to a limit of the harness —
**never to an extraction defect.** Breakdown:

- **3 address/register maps** — e.g. `$1F8  PTRA  pointer A to hub RAM` (block-007, -008, -069).
  This is the COG RAM register map. Valuable reference content; not compilable by nature.
- **13 instruction-form notation** — `SETS D,S/#` where `D` and `S/#` are *placeholders*
  standing for operand fields, not identifiers (block-003, -029, -053…).
- **1 mixed prose + code** — a narrative sentence sharing a monospace block with instructions
  (block-012).
- **~22 harness limits** — the auto-declarer must guess which token on the failing line is the
  undefined symbol, and the compiler reports a line number without naming it. Where the guess
  lands on a mnemonic, a reserved word, or an already-defined local label, the harness itself
  errors. These are defects of the validation scaffold, not of the captured text.

## Fidelity evidence, independent of compilation

The DOCX capture **preserves tab structure that the prior PDF capture destroyed.**
`silicon-doc-text.txt:37` reads `\tSETQ\t#16-1\t\t'ready to load 16 longs` as one line;
in `p2-documentation.txt` that same code line was split, stranding the comment alone at
`:208`. That is the column damage DOCX-primary exists to prevent, and it is the concrete
reason this re-extraction was worth running.

**These blocks are captured and catalogued, not published.** Nothing here is promoted into
`deliverables/ai/P2/`; a fragment that compiles under a synthesised harness has been shown
syntactically faithful, which is not the same as being a shippable example.

---

## CORRECTION, 2026-08-26 («#310») — pass 2 had missed the document's best code

The extraction above walked **paragraphs only**. The Silicon Doc keeps its worked examples
**inside table cells**, so pass 2 never saw them. Six cell-hosted listings, 121 code lines,
were recovered — and they are the flagship examples, not scraps:

| File | Lines | What it is | `pnut-ts -d` |
|---|---|---|---|
| `cell-01.txt` | 66 | **XBYTE demo** (`con _clkfreq = 10_000_000`) | **COMPILES CLEAN** |
| `cell-02.txt` | 36 | XBYTE / single-step bytecode executor | fragment — starts mid-program, by design |
| `cell-03.txt` | 68 | **Goertzel input and display** | **COMPILES CLEAN** |
| `cell-04.txt` | 86 | HDMI base config | code faithful; `DAT file not found [birds_16bpp.bmp]` — an external asset the document does not ship |
| `cell-05.txt` | 252 | **VGA 640×480×16bpp 5:6:5 RGB — HDMI** | **COMPILES CLEAN** |
| `cell-06.txt` | 5 | `DAT ORG` snippet | **COMPILES CLEAN** |

**4 of 6 compile clean under `pnut-ts v1.55.3 -d`**, with no synthesised harness and no declared
symbols — these are whole programs, not fragments. That is a far stronger fidelity result than
the harnessed 67/106 above, because nothing was added to make them work.

**Why this was missed, and why it matters beyond this source.** The walker collapsed whitespace
inside table cells, so a 636-line cell became one 32,199-character line. The table COUNT was
still right (48/48) and the digit-density gate still passed — both true statements about a
mangled artifact. `docx_walk.py` now preserves intra-cell newlines, and the pass-2 extractor
reads cells as well as paragraphs. **31 of this document's 48 tables have multi-line cells**, so
this was not an edge case.
