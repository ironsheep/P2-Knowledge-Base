# Licensing decision record

**Decided:** 2026-08-08
**Applies to:** every published document, every repository statement, and the
shipped knowledge base.
**Status:** authoritative. The canonical text in §5 is what the publish gate
checks against.

---

## 1. The decision

| What | License |
|---|---|
| **Documents** — manuals, guides, app notes, PDFs | **CC BY-SA 4.0** |
| **Code and data** — YAML, Python, scripts, templates | **MIT** |

Documentation is licensed **Creative Commons Attribution–ShareAlike 4.0
International**. Readers may share and adapt the material for any purpose,
including commercially, provided they give attribution and license their
adaptations under the same terms.

---

## 2. Why BY-SA, and not NC-ND

Between 2026-06-07 and 2026-08-08 the documents carried **CC BY-NC-ND 4.0**,
added with a "contact us for commercial use" clause. The intent behind that
change was narrow: to prevent someone reselling the manuals as their own
product. The instrument was wrong for the goal, in three ways.

**It was broader than intended.** NonCommercial does not restrict resale — it
restricts *all* commercial use. A training company referencing a manual in a
paid course, a distributor bundling a PDF with a board, a consultant handing a
chapter to a client: all disallowed. NoDerivatives went further still,
blocking translations, excerpting, and community forks — the exact uses a
knowledge base exists to enable.

**It was not what contributors saw.** The first Community Review editions
(2025-12-09) shipped **CC BY-SA 4.0**, and every edition through 2026-05-22 ran
that way. People contributed corrections, review, and hardware verification to
an openly-licensed work. Changing the terms afterward asked them to accept
retroactively narrower conditions than the ones they volunteered under.

**It contradicted our own standard.** `manual-front-matter-and-code-coloring-standard.md`
specified CC BY-SA 4.0 throughout and was never amended. The documents drifted
from the governing standard and stayed out of compliance with it for two
months. That is a process failure, and §6 records what now prevents it.

**It also constrained the co-holder.** The manuals are jointly copyrighted
Iron Sheep Productions, LLC and Parallax Inc. Under NC-ND, Parallax needed
permission to ship documentation Parallax co-owns — in kits, educational
packages, distributor bundles, or translations.

**Nothing was retroactively taken.** Creative Commons licenses are
irrevocable. Every copy distributed under BY-SA remains BY-SA permanently, and
copies distributed under NC-ND remain available under those terms too. No
reader lost a right they already held.

### Why not CC BY 4.0

CC BY was genuinely considered — it imposes no copyleft and is closest to the
instinct to impose no license at all. BY-SA was chosen because it restores
precisely what contributors and readers saw, and because ShareAlike keeps
adaptations of community-verified material open to the community that verified
it. The cost is real and accepted: an adaptation of this material must itself
be BY-SA, and that binds both copyright holders equally.

---

## 3. Trademark is the right tool for the resale concern

Copyright was the wrong instrument for "don't resell this as your own." The
right one is trademark and trade dress. A reuser may copy, adapt, translate,
and sell the text — but may not present the result as the official Iron Sheep
or Parallax edition, or use those names, logos, or cover trade dress to imply
endorsement.

Trademark rights in the United States arise from use in commerce and do not
require registration. The trademark statement in §5 therefore makes no claim of
registered status; it states what the license does and does not grant.

---

## 4. Licensing statements do not belong in the knowledge base

The shipped YAML under `deliverables/ai/P2/` states **no licensing terms —
neither ours nor anyone else's.**

The test for anything in that tree is whether it helps an agent write better P2
code. Licensing metadata fails it. Our own terms are repository metadata that
had been copied into the payload, where they were the one place stale terms
were *actively served* to remote agents. Third-party terms — OBEX object
licenses, board licenses — were worse: hand-mirrored copies of facts we do not
own and cannot keep current.

The evidence was decisive. Of 35 OBEX `license:` values, **21 said "Other"**
(no information), **13 were malformed** (`MITTags`, `OtherTag`, `MITTag` —
scraper artifacts concatenating the value with the next field name), and
**one** was both correct and useful. The fields sat under `metadata:` and
`provenance:`, beside scrape bookkeeping — never curated. An agent parsing
`MITTags` receives a license that does not exist, and a wrong license claim
about someone else's code is worse than no claim at all.

The authoritative statement travels with the artifact anyway: the P2 source
file convention requires a `Terms of Use` block in every `.spin2` file, and
`p2kb_obex_download` hands the agent that source. Removing the mirror also
removes a permanent drift channel — licensing will never need sweeping through
the YAML tree again.

**The rule:** *the knowledge base never states licensing terms as fact —
neither ours nor anyone else's. It may teach an agent how to write one.*

That last clause is not a loophole. `p2-source-file-organization-standard.yaml`
keeps its license content because it is a **template** showing an agent how to
write the license footer of a `.spin2` file it authors, with
`Copyright (c) YYYY Your Legal Name` as a fill-in. It helps produce a better,
convention-correct source file, so it passes the test on the merits.

---

## 5. Canonical text

These are the exact forms. The publish gate checks documents against them.

Two forms, by document class. A manual has front matter with room for the full
grant; an app note is 5–20 pages and states the same terms compactly. **Both
are canonical** — the difference is deliberate, not drift. What must never vary
is the license itself, the URL, and the trademark scope sentence.

### 5.1 Manuals and guides — full block, jointly held works

Heading: `# Copyright and License`.

```markdown
Copyright © <year(s)> Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0).

You are free to:

- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially

Under the following terms:

- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

To view the full license, visit: https://creativecommons.org/licenses/by-sa/4.0/

### Trademarks

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC or Parallax Inc.
```

**Copyright years are per-document and intentionally vary** (2025, 2025–2026,
2026) — they record when that work was authored and are never normalized.

**There is no "contact us for commercial use" clause.** BY-SA permits
commercial use; a clause inviting people to ask permission for something the
license already grants is contradictory. It was removed everywhere.

### 5.2 App notes — compact block

Heading: `## Copyright & License`. Three paragraphs, no bullet list.

```markdown
Copyright © <year(s)> Iron Sheep Productions, LLC and Parallax Inc.

This work is licensed under the Creative Commons Attribution–ShareAlike 4.0 International License (CC BY-SA 4.0) — you may share and adapt it, including commercially, with attribution and under the same terms. To view the full license, visit <https://creativecommons.org/licenses/by-sa/4.0/>.

Parallax, Propeller, and Spin are trademarks of Parallax Inc. This license grants permissions under copyright only; it does not grant rights to use these trademarks, and adapted or redistributed copies must not imply endorsement by, or official status with, Iron Sheep Productions, LLC or Parallax Inc.
```

Before this record, the seven published app notes carried **three different
structures** — P2AN001–004 in three paragraphs, P2AN005–007 compressed into a
single run-on line mixing copyright, license, and trademarks. All seven now use
the form above.

### 5.3 Document front matter — ISP-only works

Documents with no Parallax co-copyright (for example the PNut-Term-TS User
Guide) use the same block with the holder line reading:

```markdown
Copyright © <year(s)> Iron Sheep Productions, LLC.
```

and the trademark sentence adjusted to name Iron Sheep Productions, LLC alone
as the party whose endorsement must not be implied. The Parallax trademark
notice remains, because these documents still discuss Parallax products.

**ISP-only documents carry the same license as the rest of the shelf.** They
are separable in principle, but an inconsistent license across a published
shelf costs more than the separation is worth.

### 5.4 Repository README

```markdown
## License

This project is dual-licensed:

- **Documentation** (manuals, guides, app notes, PDFs): [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — share and adapt, including commercially, with attribution and under the same terms.
- **Code and data** (YAML, Python, scripts, templates): [MIT License](LICENSE)

Documents © 2024–2026 Iron Sheep Productions, LLC and Parallax Inc. Code and data © 2024–2026 Iron Sheep Productions, LLC.

Parallax, Propeller, Spin, and the Parallax logo are trademarks of Parallax Inc.
```

### 5.5 Contributor terms

```markdown
## License

By contributing, you agree that your contributions are licensed under the terms
this project publishes under: **MIT** for code and data, and **CC BY-SA 4.0**
for documentation. These are the same terms your contribution ships under —
we do not ask contributors for broader rights than we grant readers.
```

The final sentence is the point. Asking contributors for permissive terms
while shipping restrictive ones was the specific asymmetry that made the NC-ND
change indefensible, and the statement should make its absence explicit.

---

## 6. What prevents recurrence

1. **This record** is the single source of truth. Every licensing statement in
   the repository quotes §5 rather than restating it from memory.
2. **The templates carry the canonical block** —
   `manual-front-matter-and-code-coloring-standard.md` (which was correct all
   along) and `APP-NOTE-CREATION-GUIDE.md` (which was not). A new document
   inherits correct terms by default.
3. **A publish gate checks it.** `engineering/tools/validation/audit-license-block.py`
   verifies that every document source carries the §5 text before release.
   License drift reached 17 documents and shipped publicly for two months
   because nothing checked. Every other class of render defect we have been
   bitten by now has a gate; this one does too.

---

## 7. Copyright holders differ by bucket

The two licenses do not cover the same authorship, and the holder lines
reflect that:

| Bucket | License | Copyright |
|---|---|---|
| **Documents** — manuals, guides, app notes, PDFs | CC BY-SA 4.0 | Iron Sheep Productions, LLC **and Parallax Inc.** (jointly authored) |
| **Code and data** — YAML, Python, scripts, templates | MIT | **Iron Sheep Productions, LLC** alone |

The root `LICENSE` previously read `Copyright (c) 2024 Parallax Inc.` — a stale
year, and the wrong holder entirely for the bucket it governs. It now reads
`Copyright (c) 2024-2026 Iron Sheep Productions, LLC` (confirmed 2026-08-08).

Do not "correct" the MIT holder line to match the document copyright. The
asymmetry is deliberate: the documents are a joint work, the tooling and
knowledge base are not.
