# TAQOZ Bit Bashers Guide — Extraction Audit

**Source:** `The Bit Bashers Guide to the Parallax P2 ~  Using TAQOZ ROM Forth.docx` — 13,808,977
bytes. **Extraction date:** 2026-08-26. **Mode:** first full ingestion (row sat at 25%, queued
since 2026-06).
**Tooling:** `engineering/tools/extraction/docx_walk.py` · `audit-extraction-digit-density.py`.
**`pnut-ts` deliberately NOT run** — see Pass 2.

## Scope — and what this source is NOT

This documents **TAQOZ ROM Forth**, the Forth interpreter resident in P2 ROM. It is **not** a Spin2
or PASM2 reference, and its code examples are **Forth**.

**Relationship to the `taqoz` row — checked, and reported rather than decided.** The task asked me
not to conflate the two and to *say so as a finding* if they turn out to be the same corpus.
**They are one logical source.** The dashboard's `taqoz` row already says so: it is marked
**`🟡→🏆`** with *"authoritative `.docx` now staged: `sources/TAQOZ-Forth-Bitbashers-Guide/`"*, and
the queue row at `:146` schedules this ingestion as that upgrade.

So `sources/taqoz/` holds **preliminary web research** (`taqoz-web-research-preliminary.md`,
unverified) and this folder holds the **authoritative guide** that supersedes it. Two folders, two
artifact tiers, **one dashboard row** — which is why the row's authority column carries an arrow
rather than a single symbol. The folders are **not merged here**; that is a registry decision and
belongs to «#318»'s reconciliation sweep.

## Structural survey

| | |
|---|---|
| `<w:p>` paragraphs | 710 |
| `<w:tbl>` tables | **54** (0 nested; **33 with multi-line cells**) |
| `word/media` | **25** (13 MB — the bulk of the file) |
| `word/comments.xml` | **present — 2 comments** |

**A prediction this pass got wrong, recorded rather than quietly dropped:** 54 tables against 710
paragraphs suggested the content would live mostly *in* tables. Measured, only **16,430** of
**65,256** text characters are inside cells. The document is prose-and-figures; its size is the
25 images, not its tables.

## Digit-density gate (§2a)

| artifact | lines | w/digit | density |
|---|---|---|---|
| `taqoz-bitbashers-text.txt` | 613 | 400 | **65.3%** |
| `complete-taqoz-bitbashers-reference.md` | 570 | 355 | 62.3% |

**Exit 0.** The tool's caveat travels with it: total numeral loss only, blind to partial loss, never
a completeness certificate.

## Coverage

54/54 tables, 47 headings, 25/25 media extracted losslessly from `word/media`. Document order
preserved; intra-cell newlines preserved (33 tables need it).

**Per-figure catalog (added 2026-09-10):**
[`assets/images-taqoz-bitbashers-2026-08-26/image-catalog.md`](assets/images-taqoz-bitbashers-2026-08-26/image-catalog.md).
Extraction accounted for the 25 media here from the start; the catalog that says *what each one
is* was pass 3's deliverable and had not been written. It records one substantive follow-up:
**10 of the 25 figures are QR codes**, and the URLs they encode are invisible to the text
extraction — decoding them needs a QR reader this container does not have.

## Pass 2 — code: capture-and-catalogue, NOT compiler-validated

**The code in this guide is Forth.** `pnut-ts` compiles Spin2/PASM2 and **cannot** validate Forth;
running it would produce a page of failures that say nothing about extraction fidelity and would
misrepresent faithful text as broken. **It was not run, and that is a deliberate scope decision, not
a skipped step.**

Forth listings are captured in `taqoz-bitbashers-text.txt` and the curated reference in document
order with whitespace intact. A future dedicated Forth pass could validate them against a TAQOZ
interpreter; nothing here claims they are validated.

**Where the guide describes P2 SILICON rather than Forth syntax** — ROM residence, boot interaction,
the serial console, pin access — that content **is** cross-checkable against `silicon-doc`, and this
task was sequenced after the silicon-doc completion for exactly that reason.

## Pass 6 — findings

**2 comments, both substantive, both anchored to the same `(not in ROM)` paragraph.** Detail in
`reviewer-comments-harvest-2026-08-26.md`.

**F-370 filed.** **Peter Jakacki, the author of TAQOZ**, states ROM TAQOZ is *"not only a cut-down
version but also **an early version**"*. Our `architecture/boot-rom/taqoz-forth.yaml` calls it *"the
finite, fixed version"* — correct as far as it goes, and it misses the consequence: **a word present
in both ROM and RELOADED may differ in behaviour, not just in presence.**

**Noted as actionable:** that same YAML's `rom_vs_reloaded_word_diff` gap carries the chase *"Extract
ROM dictionary from `ROM_Booter.lst`"* — and we **hold** `ROM_Booter.lst` (411,535 bytes, 48 TAQOZ
mentions). The first half of that chase needs no new source and has never been run.

**Gap ledger, both halves.** Opened: none new — the ROM/RELOADED word-set question is already
tracked by `taqoz-forth.yaml`'s own gap, and duplicating it into `KNOWLEDGE-GAPS.md` would create
two homes for one question. Closed: none.

## Trust

**🟡 cross-check.** Community-authored (not Parallax), but by the language's own author, and the
document is explicit about its ROM scope. Its P2-silicon statements are corroboration material;
its Forth semantics are authoritative for TAQOZ and out of scope for the P2 KB proper.
