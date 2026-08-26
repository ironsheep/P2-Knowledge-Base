# TAQOZ Bit Bashers Guide — reviewer-comment harvest

**Source:** `word/comments.xml` · **Harvested:** 2026-08-26 · **2 comments**, both paired to their
anchor via `commentRangeStart`/`End`.

**Both anchor to the same paragraph** — the one the guide itself marks `(not in ROM)`:

> *"Double numbers are two 32-bit stack entries which are treated as one 64-bit value and can be
> specified by ending the number with a dot. **(not in ROM)**"*

| # | Author | Date | Note | Route |
|---|---|---|---|---|
| **0** | Anonymous | 2023-03-30 | *"This did not work for me. I got `??? .D ???` instead of `--- 1234...`"* | context for [1] — a reader hitting the documented ROM limit in practice |
| **1** | **Peter Jakacki** | 2023-04-06 | *"The ROM version is not only a cut-down version but also **an early version**. Use ROM version for debugging hardware etc especially when you can't seem to load the RELOADED version which can then be backed up to Flash or SD."* | **F-370** |

## Why [1] carries weight

**Peter Jakacki is the author of TAQOZ.** For TAQOZ specifically he stands where Chip Gracey stands
for P2 silicon — this is designer testimony inside the document's own review thread, not a forum
lead. Two things in it are new to our tree:

1. **ROM TAQOZ is an *early* build, not merely a subset.** Our `taqoz-forth.yaml` says *"the finite,
   fixed version"*, which invites the assumption that a word present in both ROM and RELOADED
   behaves the same in both. The author's wording says otherwise. → **F-370**.
2. **Usage guidance:** use ROM TAQOZ for hardware debugging, especially when RELOADED will not load.
   Practical, and nowhere in our tree.

## The ROM/RELOADED boundary is not systematically marked

Measured: the guide carries **one** `(not in ROM)` marker, while referring to TAQOZ RELOADED at
`:287`, `:430`, `:594`, `:654`, `:671` and `:799`. So the boundary is discussed throughout and
flagged in exactly one place — which is how comment [0]'s author found it, by trying it.

**This is not filed as an erratum.** The guide's title is *"Using TAQOZ **ROM** Forth"* and it never
claims to be a RELOADED reference; marking every ROM/RELOADED difference is beyond what it sets out
to do. It is recorded here as a **known reading hazard** of the source, and it is already tracked
from the KB side by `taqoz-forth.yaml`'s own `rom_vs_reloaded_word_diff` gap.
