---
title: Silicon Notes Filter Test
---

# Chapter 1: Prose Cases

## Plain paragraph

CASE-POS-PARA. [Rev C]{.silicon-note topic="Paragraph note"} A note at the start of a
sentence in an ordinary paragraph, with 50% and a_b in the prose after it.

CASE-POS-MID. A first sentence. [Rev C]{.silicon-note topic="Mid-paragraph note"} A note
that starts the second sentence of a paragraph.

## Inside a blockquote

> CASE-POS-QUOTE. A trap callout written as a blockquote.
> [Rev C]{.silicon-note topic="Blockquote note"} The note inside it.

## Inside a list

- CASE-POS-LIST. [Rev C]{.silicon-note topic="List-item note"} A note in a bullet.

# Chapter 2: Edge Cases

CASE-EDGE-NOTOPIC. [Rev C]{.silicon-note} A note with no topic: the index falls back to
this section's title, and the build log carries a warning.

CASE-NEG-OTHERSPAN. [plain text]{.other-class} An unrelated span: it must NOT be tagged
and must NOT appear in the index.

CASE-NEG-BRACES. Prose braces {.notattr} stay literal text.

| Column | Value |
|---|---|
| CASE-EDGE-TABLE | [Rev C]{.silicon-note topic="Table-cell note"} keeps its tag |

# Appendix A: Silicon Notes

CASE-INDEX. The index below must list six entries in document order (paragraph, mid,
blockquote, list, no-topic, table-cell), each linked to its note, and nothing else.

::: silicon-note-index
:::
