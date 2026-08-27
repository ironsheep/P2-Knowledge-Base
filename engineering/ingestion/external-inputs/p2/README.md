# `external-inputs/p2/` — a staging area, not a source registry

This folder holds **original vendor documents that landed here on the way in**. It is staging.
It is **not** a source folder, and nothing here is a citable locator:

- no dashboard row in `engineering/ingestion/README.md`
- no extraction audit, no cross-source analysis
- no trust tier in `engineering/ingestion/AUTHORITATIVE-SOURCES.md`

Tiers, audits and citable `path:line` locators belong to `engineering/ingestion/sources/<slug>/`.
**Cite the `sources/` copy. Never cite a file in this folder.**

Several files here are *also* present under `sources/`, under the **same filename**. Two of those
pairs are not the same bytes, and one of them is not the same document (see below). Check this
table before opening anything here.

## What is here, and where its canonical copy lives

| File in this folder | Canonical source folder | Relationship |
|---|---|---|
| `Parallax Propeller 2 Documentation v35 - Rev B_C Silicon.docx` | `sources/silicon-doc/` (same filename) | **DIFFERENT DOCUMENT — the copy here is NOT authoritative.** See below. |
| `Propeller 2 Hardware Manual - 20221101.docx` | `sources/p2-hardware-manual/` (same filename) | Same edition exported twice. Extracted text is identical (3,026 paragraphs / 145,487 characters both). The two files differ only in the container format of two embedded images (`word/media/image23` and `image31`, PNG↔GIF). Recorded in `DOCUMENT-LINEAGE.md`; canonical = the `sources/` copy. |
| `Propeller 2 Assembly Language (PASM2) Manual - 20221101.docx` | `sources/pasm2-manual/` (same filename) | Byte-identical (md5 `44b7b464df645a490bfd6f8e27fe7557`). Staged there 2026-08-26 for the DOCX-primary re-ingestion. |
| `P2-Assembly-Language-PASM2-Manual-Draft-221117.pdf` | `sources/pasm2-manual/` (same filename) | Byte-identical (md5 `914077a57dcd2d3b8c5ff9696f93f472`). |
| `Parallax Spin2 Documentation v51.docx` | `sources/spin2-v51/` | **Un-staged primary.** That folder holds the v51 *PDF* (`P2 Spin2 Documentation v51-250425.pdf`) and its derived text; the DOCX exists only here. (The current Spin2 edition is `sources/spin2-v55/`, which has its own DOCX.) |
| `P2 Spin Manual Draft 20240607.docx` | derived work lives in `sources/spin2-v51/` (`spin-manual-draft-2024-extraction.md`, `spin-manual-draft-2024-complete-audit.md`) | **Un-staged primary.** No `sources/` folder holds this document; only the 2025-08-15 extraction/audit of it exist, filed under `spin2-v51`. |
| `Propeller 2 Questions & Answers.xlsx` | `sources/p2-qa-spreadsheet/` | **Un-staged primary for the `p2-qa-spreadsheet` row.** That folder holds only `qa-spreadsheet-extraction.md` and `qa-spreadsheet-complete-extraction-audit.md` — the spreadsheet they were made from is this file. The source row is *not* blocked for want of a primary document. |
| `quarantine/P2 The Bit Bashers Guide to the Parallax P2 _ Using TAQOZ ROM Forth.pdf` | `sources/TAQOZ-Forth-Bitbashers-Guide/` | Image-only PDF of the same guide, quarantined — see `quarantine/README-DANGER.md`. The guide was ingested 2026-08-26 from the **DOCX** in that source folder; use the DOCX. |
| `quarantine/README-DANGER.md` | — | The quarantine notice itself. |

## The Silicon Doc DOCX here is NOT authoritative

Same filename as `sources/silicon-doc/`, different content: 4,919,444 bytes here vs 4,814,991 bytes
there. Both carry 48 tables and 34 media, so a structural check calls them identical. Extracted
paragraph text differs at **four sites**, and the copies **disagree on a flag semantic**:

**GETBRK D WZ — the Z assignment.**

- `sources/silicon-doc/` (canonical, and what the 2026-08-26 re-extraction was made from):
  `Z = 1 if no SKIP/SKIPF/EXECF/XBYTE pattern queued (D = 0) or 0 if pattern queued (D <> 0)`
  — extracted at `sources/silicon-doc/silicon-doc-text.txt:2591`
- **this folder's copy**: `... (D = 0) or **1** if pattern queued (D <> 0)`

The copy here sets `Z = 1` in **both** branches, which makes `WZ` carry no information on an
instruction that requires a flag effect. The canonical copy gives `Z = 1 / Z = 0`.

**The other three sites** (canonical reading first):

- a smart-pin paragraph the copy here **does not contain at all** — *"Once a smart pin is configured
  via WRPIN and then started by making its DIR bit high, it can be reset at any time by making its
  DIR bit low. It does not lose its configuration set by the last WRPIN…"*, the paragraph that also
  explains the 126 bits of smart-pin state (`silicon-doc-text.txt:3856`)
- PWM dither rationale: *"a maximum of only two **adjacent 8-bit DAC levels are set** for every 256
  clocks"* vs *"a maximum of only two **transitions occur** for every 256 clocks"*
- a typo the canonical copy has and this one does not: `cog regis+ters:` vs `cog registers:`

Recorded as **F-367** in `engineering/operations/P2KB-CORRECTION-FINDINGS.md`. What to do about the
duplication — delete, reconcile, or keep both — is **Stephen's call and has not been made**. This
file exists so that whoever opens the wrong copy is told before they cite it.

## Adding something here

Dropping a document in this folder does not ingest it. Run `ingest-source`, which stages the
primary into `sources/<slug>/`, assigns a tier in `AUTHORITATIVE-SOURCES.md`, records lineage in
`DOCUMENT-LINEAGE.md`, and adds the dashboard row. Add a row above when a file lands here so the
mapping stays complete.
