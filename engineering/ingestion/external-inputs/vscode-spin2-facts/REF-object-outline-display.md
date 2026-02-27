# Object Outline Display Guide

This document describes how the VSCode Outline panel is populated for Spin2/Spin1 files. The outline shows section blocks (CON, VAR, OBJ, DAT, PUB, PRI) and, for some of them, an associated comment. Understanding exactly what gets displayed — and what doesn't — is essential for writing well-structured code.

## How It Works

The outline is produced by a three-stage pipeline:

1. **Document Symbol Parsers** scan each source line, build `OutLineSymbol` objects, and store them in the document findings cache.
   - `server/src/parser/spin2.documentSymbolParser.ts` (for `.spin2` files)
   - `server/src/parser/spin1.documentSymbolParser.ts` (for `.spin` files)
2. **DocumentSymbolProvider** (`server/src/providers/DocumentSymbolProvider.ts`) converts those objects into LSP `DocumentSymbol` responses. It is a straight pass-through — no comment logic lives here.
3. **VSCode** renders the Outline panel from the symbols.

All comment-related decisions happen in step 1, in the parsers.

## Section Headers: CON, VAR, OBJ, DAT

For these four section types, a comment on the section header line **is included in the outline label**. The comment text — including its delimiters — is concatenated directly onto the section keyword.

### Comment Recognition

The parser checks for comments on the section header line. Either form of non-doc comment is recognized:

1. **Brace comment `{ text }`** — Uses `line.indexOf('{')` and `line.indexOf('}')`. Both the opening `{` and closing `}` must appear on the same line. The captured text runs from `{` through `}` inclusive.

2. **Tic comment `' text`** — Uses `line.indexOf("'")`. The captured text runs from the `'` through end of line, including the `'` itself.

**If both appear on the same line, the leftmost comment wins** regardless of type.

### What Appears in the Outline

The label is built as: `SECTION_KEYWORD + ' ' + commentText`

| Source Line | Outline Label |
|---|---|
| `CON { Motor Constants }` | `CON { Motor Constants }` |
| `VAR ' Instance Variables` | `VAR ' Instance Variables` |
| `DAT` | `DAT ` (keyword + trailing space, no comment) |
| `OBJ { objects } ' more info` | `OBJ { objects }` (leftmost wins) |

The detail/description field is always empty for section headers.

### What Does NOT Work

- A comment on the line **above** the section keyword is invisible to the outline.
- If `{` appears with no matching `}` on the same line (e.g., the start of a multi-line block comment), no brace comment is captured.
- `{{ }}` doc comments are not specifically handled here. If `{{ text }}` appears on a section line, the first `{` and first `}` are found, which captures `{ text }` (the inner content between the first brace pair). This is an incidental match, not intentional support.

## Method Declarations: PUB, PRI

For PUB and PRI methods, comments are **actively stripped** from the outline. Only the method name, parameters, and return values survive.

### Stripping Logic

The parser takes everything after the PUB/PRI keyword and sequentially removes:

1. **Tic comments** — Splits on `'`, keeps only the part before it
2. **Brace comments** — Splits on `{`, keeps only the part before it
3. **Local variables** — Splits on `|`, keeps only the part before it

| Source Line | Outline Label |
|---|---|
| `PUB start(pin, freq)` | `PUB start(pin, freq)` |
| `PUB start(pin) ' Start motor` | `PUB start(pin)` |
| `PUB start(pin) { motor } \| tmp` | `PUB start(pin)` |

### Detail Field (Spin2 Only)

In Spin2, PUB entries show `"Public"` and PRI entries show `"Private"` as secondary detail text. In Spin1, the detail field is empty.

## Lines the Outline Never Sees

Before any comment extraction, a state machine skips entire lines that are pure comments:

| Line Form | Outcome |
|---|---|
| `' text` (starts with single tic) | Entire line skipped |
| `'' text` (starts with double tic) | Entire line skipped |
| `{{ text }}` (single-line doc comment) | Entire line skipped |
| `{{ ... }}` (multi-line doc comment block) | All lines within the block skipped |
| `{ ... }` (multi-line block comment) | All lines within the block skipped |
| Whitespace-only lines | Skipped |

Only lines that **begin with a section keyword** (CON, VAR, OBJ, DAT, PUB, PRI) in column 1 are candidates for outline entries.

## DAT Section Children

DAT sections can contain child items in the outline: global PASM labels. These are identifiers in column 1 of DAT/PASM lines that are:
- Not reserved words or instructions
- Not data storage declarations (e.g., `BYTE`, `WORD`, `LONG` followed by data)
- Not local labels (starting with `.` or `:`)
- Not debug directives

These child labels appear nested under their parent DAT entry. No comments are associated with child labels.

Spin2 also supports inline PASM labels (from `ORG`/`ORGH`/`ORGF` blocks inside PUB/PRI methods) as outline children. Spin1 does not have inline PASM.

## Summary of SymbolKind Icons

| Section | Icon Kind |
|---|---|
| CON | Method |
| VAR | Variable |
| OBJ | Class |
| DAT | EnumMember |
| PUB | Method |
| PRI | Field |
| DAT/PASM global labels | String |

## Guidelines for Outline-Friendly Code

1. **To label a section in the outline**, put a comment on the same line as the section keyword:
   ```spin2
   CON { Motor Constants }
   VAR ' Instance Variables
   ```

2. **Either `{ }` or `'` works** for section labels — use whichever fits your style. If both appear, the leftmost is captured.

3. **Comments above or below** the section keyword line do not appear in the outline.

4. **PUB/PRI comments never appear** in the outline regardless of form — keep method documentation in doc comments (`''`) for use by other tools like the interface document generator.

5. **Only one level of nesting** is supported — DAT/PASM labels nest under their parent DAT section, but there is no deeper hierarchy.
