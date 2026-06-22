---
name: ingest-source
description: >-
  Ingest a source document into the P2 knowledge base — the INGESTION head's
  front-to-back process. Use when the user says "ingest <doc>", "re-study the
  <doc>", "add a new source", "do the next ingestion", or supplies an updated
  edition of an already-ingested source (e.g. Spin2 v55 superseding v51).
  Orchestrates all passes a complete document needs — content, code examples,
  images/visual catalog, post-processing, validation, cross-source Q&A +
  conflict detection, and dashboard registration — at CURRENT tooling
  capability (DOCX-primary, pnut_ts-validated code, image-tools-mcp). Routes
  any P2KB content conflict it surfaces to the corrections register. Does NOT
  edit deliverables/ai/P2/ YAML directly (that is yaml-knowledge-base-maintenance).
---
<!-- Requires MCP: todo-mcp (head pointer + tasks); image-tools-mcp (image pass); filesystem. Uses pnut_ts compiler. -->

# Ingest a source

This is the **INGESTION head**'s working skill — the execution counterpart to
`whats-next` (which routes here) for `active_element = ingestion:<src>`. The
manual head has `prepare-manual`/`release-manual`; the YAML head has
`yaml-knowledge-base-maintenance`; **this is the ingestion head's.**

## The methodology lives in `engineering/ingestion/`, not here

This skill **orchestrates** the established methodology; it does not restate it.
Each pass below points at its canonical doc. Read the pass's doc when you enter
that pass. The standing docs:

| Doc | Role |
|---|---|
| `methodology/source-ingestion-methodology.md` | master methodology + **Cross-Source Q&A Audit** (questions / conflicts / trust) |
| `work-modes/document-ingestion-focused.md` | step-by-step + the **5-pass validation framework** + task scaffold |
| `methodology/source-code-extraction-methodology.md` | code-example pass |
| `methodology/image-extraction-methodology.md` | image pass |
| `methodology/ingestion-pipeline/ingestion-audit-protocol.md` | completeness verification |
| `INGESTION-UPDATE-WORKFLOW.md` | propagating an update to central-analysis docs |
| `README.md` | the **ingestion dashboard** — source registry + completeness/gates (the head's status home) |
| `AUTHORITATIVE-SOURCES.md` | trust catalog — per-source tier (the dashboard's Auth column reads from here) |
| `DOCUMENT-LINEAGE.md` | editions/supersession + source→output + derived cross-source facts |
| `KNOWLEDGE-GAPS.md` | the moving **gap ledger** + **questions-for-experts** (pass-6 output home) |

> **This skill is written to current tooling and SUPERSEDES two legacy
> constraints those docs still carry** (see §8). When this skill and a legacy
> doc disagree on tooling, this skill wins — and you update the legacy doc in
> the same pass (process fixes ship with the work that revealed them).

## Dashboards & registers — when to update each, and why

The ingestion head owns a **quad** of standing docs (+ one shared register). Update each at the pass shown — this is load-bearing: `whats-next` and the YAML head read these.

> **Certified 2026-06-12** by the **Smart Pins (Titus) rev 5** ingestion: the full quad-update flow ran
> end-to-end — `KNOWLEDGE-GAPS` routing (8 gaps G-001..008 + 3 expert-Qs Q-001..003 from 27 reviewer
> comments), reviewer-notes harvest (§5.3), conflict adjudication (#21 WRPIN selector swap confirmed vs
> silicon-doc → correctly logged as a *gap*, not a corrections-register entry, because our YAML doesn't
> carry that sub-field), and §0.6 obsolescence handling (with the refinement noted there). Dashboard +
> AUTHORITATIVE-SOURCES + DOCUMENT-LINEAGE all updated from the same run. The flow is promoted to standard.

| Doc | Update WHEN | WHY |
|-----|-------------|-----|
| `README.md` (the dashboard) | **pass 0** (add row at 0%, gates open) → **pass 7** (completeness % + gate status + the C·K·I·A·X cells) | the head's status home; `whats-next` resumes from it |
| `AUTHORITATIVE-SOURCES.md` | **pass 0 / 7** — assign the source's trust tier (new edition → re-confirm); add aliases / part-numbers for hardware | the dashboard's **Auth** column reads tiers from here; trust propagates to everything derived |
| `DOCUMENT-LINEAGE.md` | **pass 7** — record supersession (new edition), source→output (when a manual / KB area is fed), and any derived cross-source facts | the lineage half of the sacred trust chain |
| `KNOWLEDGE-GAPS.md` | **pass 6** — move the gap ledger (answered / new / still-unknown), route expert-only questions, and **harvest reviewer notes** | the moving "what we still don't know"; the dashboard's open-questions rollup reads from here |
| `P2KB-CORRECTION-FINDINGS.md` (shared register) | **pass 6** — any conflict touching *published* `deliverables/ai/P2/` YAML | hands the defect to the YAML head; this skill never edits YAML itself |

## 0. Head integration — register the element first

1. **Set the pointer:** `mcp__todo-mcp__context_set key:"active_element" value:"ingestion:<src>"` (use the source's folder slug, e.g. `spin2-v55`).
2. **Registry check (the add-new-element gate, per `whats-next` §6):**
   - New source → add a row to `README.md` (the ingestion dashboard registry; authority level, completeness 0%, gates open); stand up `sources/<src>/`.
   - **Updated edition of an existing source** (e.g. v55 over v51) → it is a *new* source folder (`sources/<src>/`), NOT an in-place overwrite of the old one. Keep the prior edition intact for diff/lineage; mark the new row, and note the supersession in `DOCUMENT-LINEAGE.md`. The old edition's extraction stays until the new one is validated and the dashboard flips authority to it.
3. **Generate the task scaffold** (`work-modes/document-ingestion-focused.md` — the 5 core `document_ingestion`-tagged tasks). Drive work with `mcp__todo-mcp__todo_next tags:["document_ingestion"]`.

## 0.5 Update / delta ingestion (an updated edition over a prior one)

When the source is a **new edition of an already-ingested source** (e.g.
Spin2 v55 over the ingested v51a), it is **not greenfield** — it is a *delta*
ingestion, and the delta is the organizing principle.

- **The document's own version-history table IS the delta roadmap.** Extract it
  first and scope the change set: every edition entry *after* the prior
  baseline (baseline = the version we previously ingested — read the prior
  source's `*-complete-extraction-audit.md`). Many doc tables also carry a
  per-version *symbol-additions* table — capture both.
- **Still extract fully** (passes 1–3) so the new edition can become the
  authority — but **drive passes 4–6 from the delta**, not the whole document.
- A delta ingestion has **two required outputs**, both load-bearing:
  1. **Additive gap-fill** — new features/methods/symbols the prior edition
     lacked. These are coverage work: the YAML head (and manuals) don't yet
     document them. Capture each with its **version gate** — the
     `{Spin2_vNN}` directive it requires, **compiler-verified at the boundary**
     (not just copied from the doc). Language version-gating is a first-class,
     **YAML-owned** fact: the P2KB YAML is its golden/canonical home, so every
     new feature must land there carrying its verified gate, and manuals derive
     gating from the YAML rather than asserting it independently (see §4).
  2. **Conflict audit (often the higher-value half)** — audit the **existing**
     prior-edition-derived content (YAML *and* manuals) **against** the new
     edition. Where they disagree, the new edition wins if it is the
     **matched-compiler authority** (e.g. pnut-ts `v1.55.0` ⇒ PNut v55), and
     each disagreement is a `P2KB-CORRECTION-FINDINGS.md` entry. A feature that
     was *extended* (e.g. a keyword that gained an operand) is a **conflict**
     against any prior text that said it had none — not merely a gap.
- **Watch the project content rules when classifying delta items.** Some
  edition changes are not findings for us — e.g. *bytecode-count* changes are
  out of scope (we don't publish compiler bytecode values). Don't open a
  conflict for something we deliberately don't document.
- **Record supersession** in `DOCUMENT-LINEAGE.md`; keep the prior edition's
  source folder intact for diff/lineage until the new edition is validated and
  the dashboard flips authority to it.
- **Sequencing:** the conflict audit should run before (or feed) any queued
  YAML-correction sprint that leans on the *old* edition's text — re-anchoring
  open findings to the new edition may confirm, refine, or overturn them.

## 0.6 Obsolescence handling — the prior information  _‹certified on the Titus rev5 run, with the refinement below›_

Every supersession **obsoletes prior information** — and the prior info is handled deliberately, **never silently dropped**. Three flavors (see `DOCUMENT-LINEAGE`): **augment** (newer edition, content grew) · **re-extraction** (prior capture was lossy) · **superseded-by-deliverable** (prior fed our manual). For each, **two kinds** of prior information must be handled:

1. **Prior source artifacts** (the old extraction files / folder):
   - **Augment** → *keep* the prior edition's folder as lineage (diff/history) — not obsolete, just no longer the authority.
   - **Re-extraction** → the prior extraction is *obsolete* (a flawed capture). **Archive it, do not delete** — move to a gitignored `archive/` with a one-line pointer to the new extraction (git history is the record). Only **after** the new extraction is validated.
     - **Refinement (Titus rev5):** the literal **archive-MOVE is gated on first redirecting any downstream references** to the prior folder — a move that strands a path referenced elsewhere is a Sacred-Rule-#7 violation. When references exist (esp. in *another head's* docs, e.g. a manual's `creation-guide.md` source table), **mark-in-place** instead: drop a `SUPERSEDED-BY-<new>.md` redirect inside the obsolete folder now, and **defer the physical move until those references are re-pointed** — which, for a manual-feeding source, happens in that manual's certification audit (the downstream re-validation in step 2). Check `git grep <folder>` before moving. _(Note: an untracked/gitignored prior folder has no git-history record — preservation MUST be by the move/marker, not by relying on history.)_
   - **Superseded-by-deliverable** → the source stays as input.
2. **Downstream derivations** (YAML entries, manual content, central-analysis matrices built from the prior info): **re-anchor and re-validate against the NEW authoritative extraction** (pass 6). Anything derived from an *obsolete/lossy* extraction is **suspect until re-checked** — a fragmented / whitespace-damaged code example may have produced wrong downstream content. Conflicts touching published YAML → corrections register; manual content → flag for the manual head. Record the supersession + what re-anchored in `DOCUMENT-LINEAGE`. **No dangling references** to archived artifacts (Sacred Rule #7 — redirect to the new).

**This run's case (Titus re-extraction):** prior artifacts = the PDF-scraped Titus extraction in `engineering/ingestion/smart-pins-catalog/` (21 recovered examples, `john-titus-extract.md` per mode, the recovery scripts, `TITUS-CODE-RECOVERY.md`). After the new DOCX extraction validates: archive those with a pointer to the new; then **re-validate any Titus-derived YAML / Smart Pins manual content against the new authoritative extraction** (this dovetails with the Smart Pins manual certification audit) — route conflicts to the corrections register; record in `DOCUMENT-LINEAGE`.

## 1. The passes a complete document needs

A "complete" ingestion is not one extraction — it is **seven passes**. All of
them are required for a new document.

| # | Pass | Output | Primary tooling (current) |
|---|------|--------|---------------------------|
| 1 | **Content** — text, tables, structure, lineage | `<src>-text.txt` + curated `complete-*.md` summaries | **DOCX** (literal char stream; clean tables); **PDF-only → `pdf2md`** (docling: recovered tables + fenced code), **`camelot` lattice** for a stubborn ruled table |
| 2 | **Code examples** — extract → validate → catalog | `assets/code-<date>/` + `CODE-EXAMPLE-EXTRACTION-MATRIX.md` row | **DOCX** extract + **`pnut_ts`** validate; **PDF-only fallback → `pdf-layout`** (preserves column/indent for code listings) then `pnut_ts` |
| 3 | **Images / visual catalog** — extract → quality-check → catalog → consumer registry | `assets/images-<src>-<date>/` + `image-catalog.md` + `INGESTION-IMAGE-EXTRACTION-MATRIX.md` row | **DOCX media** + **`image-tools-mcp`** (PyMuPDF fallback) |
| 4 | **Post-processing** — relationship matrices, specialized extractions (timing tables, narratives), pattern library | central-analysis matrices | analysis |
| 5 | **Validation** — section-by-section completeness | `<src>-extraction-audit.md` validation results | `ingestion-audit-protocol.md` 5-pass |
| 6 | **Cross-source Q&A + conflict audit** — answer prior questions, raise new, harvest reviewer notes, **flag conflicts**, score trust | Q&A audit; **gap ledger + questions-for-experts → `KNOWLEDGE-GAPS.md`**; **conflicts → `P2KB-CORRECTION-FINDINGS.md`** | corroboration matrix (§4) |
| 7 | **Registration + update propagation** | `<src>-complete-extraction-audit.md`; **`README.md` (dashboard) + `AUTHORITATIVE-SOURCES.md` (tier) + `DOCUMENT-LINEAGE.md`** updated | `INGESTION-UPDATE-WORKFLOW.md` |

## 2. Format strategy — validator-driven, not dogmatic

**Pick the format per pass on evidence, gated by a validator — never by a
hardcoded "always use X" rule.** With current tooling, **DOCX is primary for
all three extraction passes**; the PDF path is a *fallback*, not a gate — but
when a source is **PDF-only** (no `.docx` — e.g. board Product Guides), reach
for the modern PDF toolkit, not the old PyMuPDF-only path (see the PDF-only
ladder below).

- **Content (pass 1) → DOCX.** A `.docx` is a zip; `word/document.xml` is the
  literal character stream with real table structure. This avoids the
  glyph-position reconstruction that causes column-bleed (the root cause of
  several KB defects, e.g. table fragments bleeding into prose).
- **Code (pass 2) → DOCX, validated by `pnut_ts`.** DOCX carries exact
  spaces/tabs in XML — for whitespace-sensitive Spin2/PASM2 this is at least as
  faithful as PDF, and the compiler settles fidelity objectively (*extract
  exactly, validate automatically*). Use `pnut_ts -d` for any DEBUG-window
  code (a no-`-d` compile silently skips `debug()` contents). **Only fall back
  to the PDF for a specific example that fails to compile or shows visible
  whitespace damage** — diff that one example's two extractions and keep the
  faithful one.
  - **Normalize Word/Docs auto-correct substitutions before validating** —
    these silently break code and masquerade as "fragment" failures:
    - **`…` (U+2026) vs `...`** — **`...` (three ASCII periods) is a Spin2
      line-continuation marker** ("ignore rest of line, continue on next";
      added v37). Auto-correct can fold a literal `...` into the single glyph
      `…`, which the compiler rejects (`Unrecognized character $2026`).
      **Classify by context** — `…`/`...` at a code line's *end* is a mangled
      continuation → restore `...`; `…` mid-sentence is prose elision → the
      block is misclassified prose, drop it (see below).
    - **Curly quotes** `‘ ’ “ ”` (U+2018/19/201C/201D) → straight `' "`;
      **en/em dash** `– —` → `-`; **nbsp** (U+00A0) → space.
  - **Font-based code detection over-includes prose-in-monospace.** A block
    that fails to compile *and* is pure prose (descriptive sentences, `✔`/emoji,
    table cells) is **not a code example** — drop it from the example set rather
    than counting it as a validation failure. Validate, then filter.
- **Images (pass 3) → DOCX media + `image-tools-mcp`.** Unzip `word/media/*`
  for the original embedded assets losslessly — this eliminates the v3.0
  "black image / full-page capture / false success" failure class at the
  source. Fall back to PyMuPDF + coordinate-rescue only for assets not present
  in the DOCX (e.g. a figure that was a linked image).
- **PDF-only source ladder (no `.docx`).** When the source ships only as a PDF
  (most board Product Guides, datasheets), the DOCX paths above don't apply —
  use the baked-in PDF toolkit (`/opt/pdf-tools/README.md`) instead of the old
  PyMuPDF-only fallback. Most KB PDFs are digitally generated, so **skip OCR
  unless a page is actually scanned _or the text layer is corrupt_** (see the
  corrupt-text-layer note below):
  - **Content + tables (pass 1) → `pdf2md`** (docling) as the default — it
    recovers real tables and fenced code. For a stubborn *ruled* table (board
    pin maps, electrical specs), `camelot --pages all --format csv lattice
    <file.pdf>` extracts it surgically to CSV.
  - **Code listings (pass 2) → `pdf-layout`**, which preserves column/indent
    layout for whitespace-sensitive PASM2/Spin2, then validate with `pnut_ts`
    exactly as the DOCX path does.
  - **Images (pass 3) → PyMuPDF/`pdfimages`** for raster extraction, then the
    same `image-tools-mcp` catalog + quality gate as above.
  - **Scanned page (rare here) → `pdf-ocr <in.pdf> <out.pdf>`** first, then run
    `pdf2md` on the OCR'd output.
  - **Corrupt text layer = a scanned page (certified on #64004-ES, 2026-06-22).**
    A Google-Docs / Quartz / "Print-to-PDF" export can carry a **broken ToUnicode
    CMap** — the text stream decodes to a cipher (e.g. "BXV WUanVacWionV" for
    "Bus transactions", "FHDWXUHV" for "FEATURES"), often on only part of the
    doc. `pdftotext` and default `pdf2md` both trust that stream and emit garbled
    text. **Detect** with a quick `pdftotext -f 1 -l 1 <pdf> -` sample; if it
    looks ciphered/garbled, **force OCR**: `docling --force-ocr --ocr-engine
    rapidocr --to md --output <dir> <pdf>` (reads rendered pixels, ignores the
    broken stream). Forced OCR adds its own noise (lost spaces, `O`↔`0`, `l`↔`I`,
    fragile part numbers) — **cross-check fact-bearing fields** (pin maps,
    part numbers) against a second signal (the table from the broken stream
    decodes consistently; a mechanical/pad drawing; the schematic) and flag any
    residual OCR-risk strings as a gap.

```bash
# Extract DOCX media (pass 3 inputs) and inspect:
python3 - <<'PY'
import zipfile, os
src="<path-to>.docx"; out="/tmp/<src>_media"; os.makedirs(out, exist_ok=True)
z=zipfile.ZipFile(src)
for n in [n for n in z.namelist() if n.startswith("word/media/")]:
    open(os.path.join(out, os.path.basename(n)),"wb").write(z.read(n))
print(sorted(os.listdir(out)))
PY
```

## 3. The image pass with `image-tools-mcp`

`image-tools-mcp` natively does what the v3.0 methodology hand-rolled, and adds
figure-content reading the old pipeline never had. Per extracted image:

- **Quality gate** (replaces the brightness<10 black-detector): `image_dimensions` (is it a discrete figure vs a full-page mis-capture?) + `image_dominant_colors` (a failed extraction reads `#000000`-dominant; a healthy figure does not).
- **Segmentation** (replaces full-page-capture handling): `image_detect_rectangles` / `image_detect_lines` / `image_detect_text_regions` to find discrete figures / bit-field boxes / timing-diagram structure.
- **Figure content → evidence (NEW):** `image_ocr_full` / `image_ocr_region` read labels, bit-field values, register names off the diagram. Catalog them — **and use them in pass 6** to cross-validate prose/YAML against what the figure actually shows (a bit-field diagram that contradicts its caption is a finding).
- **Enhancement / debt:** `image_crop`, `image_edge_detect`, `image_vectorize`, `image_unbake_transparency` as the methodology's enhancement step requires; queue anything deferred as image-enhancement debt.

Each image gets a catalog entry (purpose, OCR'd content, consumer references)
and a row in the image-extraction matrix.

## 4. Multi-source corroboration matrix (the validation backbone)

**A finding/fact is verified only against EVERY ingested, verified source that
carries that fact-type — never the single source a prior note happened to
cite.** Triangulate; corroboration is the bar; **inter-source disagreement is
itself an outcome** to surface and reconcile by authority order
(**`pnut_ts` compiler → Spin2 spec → Silicon Doc**, with
`chip-gracey-clarifications` the tiebreaker on flag semantics).

| Fact-type | Sources to check (all that apply) |
|---|---|
| Instruction flags / encoding / WC-WZ effects | `pnut_ts` · `p2-instructions-csv` · `silicon-doc` · `pnut-ts-pasm-ref` · `chip-gracey-clarifications` |
| Instruction timing (cog/hub, fixed/variable) | `p2-instructions-csv` · `silicon-doc` · `pnut_ts` |
| Clock / HUBSET bit-fields, PLL | `silicon-doc` · `p2-datasheet` · `p2-spec-sheet` · `chip-gracey-clarifications` |
| Directives (ORG/ORGF/ORGH/FIT/FILE/BYTE) | `pnut_ts` · `spin2-v51`→`spin2-v55` (incl. grammar reference) |
| Spin2 methods / operators / constants | `spin2-v55` (matched edition) · `pnut_ts` |
| Smart-pin modes / ADC gains | `spin2-v55` · `smart-pins` · `silicon-doc` |
| Boot / loaders (Prop_Hex, serial/flash) | `silicon-doc` · `rom-booter` · `flash-loader` |
| CORDIC / QLOG / QEXP | `silicon-doc` · `spin2-v55` |
| Counters / special registers (e.g. GETCT) | `silicon-doc` · `spin2-v55` · `pnut_ts` |
| **Language version-gating** (`{Spin2_vNN}` a feature requires) | **value established by `pnut_ts` version-keyword enforcement** (probe the boundary edition where the feature begins to compile) **+ the edition's per-symbol directive table**; **recorded in the P2KB YAML, which is the golden/canonical home for gating** (`minimum_version` / `version_directive` / `requires_version`). Manuals derive gating FROM the YAML, never invent it. |

> **Edition note:** when an updated edition is ingested (v55 over v51), the
> *compiler* is the matched authority (pnut-ts `v1.55.0` = ratified against
> PNut v55). Where the older spec text and the v55 compiler disagree, **the
> compiler wins**, and ingesting the v55 spec brings the prose into agreement
> with the authority we already trust.

> **"Introduced in vNN" ≠ "enforced `{Spin2_vNN}` gate" — verify which.** A
> changelog/symbol-table edition label is the *edition of introduction*; it is
> NOT automatically a compiler-enforced version gate. The boundary-probe
> distinguishes them: a genuinely-gated feature FAILS below its gate (e.g.
> `ENDIANL` fails under `{Spin2_v41}`); an ungated one COMPILES at the default
> v41 with no directive even though it "arrived" in a later edition. **Verified
> repeatedly on the v55 delta:** `MOVBYTS` (v52) and the `NEXT`/`QUIT` integer
> form (v52) are ungated; struct *bitfields* parse under STRUCT's `{Spin2_v45}`
> while `{Spin2_v54}` is author-intent only. Record the *enforced* gate (or
> `none` + an "introduced in vNN" note), never the edition label as if it were a
> gate — F-100 is exactly this defect.

## 5. Cross-source Q&A audit (pass 6 detail)

Per `source-ingestion-methodology.md` §Cross-Source Q&A, for the new source.
**All three legs are required — the conflict leg tends to dominate attention; do
NOT ship pass 6 having only flagged conflicts.** The corpus accumulates: each
source *answers* prior holes AND *opens* new ones, so a source that surfaces
zero answered/new questions is the exception to justify, not the default.
1. **Answer prior open questions** — review `KNOWLEDGE-GAPS.md` (the gap ledger) + prior audits; mark what this source answers by moving its ledger row **OPEN→ANSWERED** (page/section ref + the edition that filled it).
2. **Raise new questions** this source surfaces → add to `KNOWLEDGE-GAPS.md` (Part A gap ledger, status OPEN).
3. **Harvest embedded reviewer notes as credible feedback** — if the source DOCX carries inline editorial notes or Google-Docs comments (`word/comments.xml`), they are **not noise**: classify each (technical question / editorial / P2-fact assertion). Technical questions → `KNOWLEDGE-GAPS.md`; assertions that touch published YAML → cross-check, conflicts → corrections register. Weigh under the source's tier (don't auto-trust a cross-check source's notes as fact). **Extraction:** `word/comments.xml` holds the comment bodies (author/date/id); the comment *anchor* (what text each is attached to) comes from the `commentRangeStart/End` id markers in `word/document.xml` — pair them so each note carries its commented context. _(Certified on Smart Pins (Titus) rev 5's 27 comments — one, #21, surfaced a real bit-field error confirmed against the Silicon Doc.)_
4. **Flag conflicts** — `Source A says … / Source B says … / Resolution (which is authoritative and why)`. **A conflict that touches published P2KB YAML is a corrections-register entry** — append it to `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (`NEEDS-VERIFICATION`) for the YAML head to work via `yaml-knowledge-base-maintenance`. This skill does **not** edit `deliverables/ai/P2/` itself.
5. **Unresolved / expert-only:** where a fact is unresolved across all eligible sources, ask the user rather than guess (plain chat — no AskUserQuestion here); if only the designer can settle it, record it in `KNOWLEDGE-GAPS.md` **Part B** (questions-for-experts + who-to-ask).
6. **Update trust scoring** (HIGH multi-source-confirmed / MEDIUM single-source / LOW conflict-or-gap).

## 6. Output layout (mirror the canonical source folder)

```
engineering/ingestion/sources/<src>/
├── <src>-text.txt                      # pass 1 raw text extract
├── complete-*.md / *-reference.md      # pass 1 curated summaries
├── <src>-extraction-audit.md           # pass 5 validation results
├── <src>-complete-extraction-audit.md  # pass 7 the audit of record
└── assets/
    ├── code-<date>/                    # pass 2 validated examples
    └── images-<src>-<date>/            # pass 3 images + image-catalog.md
```

## 7. Hand back

Report:
- Passes completed (1–7) and per-pass counts: paragraphs/tables, code examples (extracted / pnut_ts-validated / failed), images (extracted / quality-passed / OCR-cataloged).
- Completeness % + gate status written to `README.md` (the dashboard).
- Q&A audit summary: prior questions answered, new questions, **conflicts routed to `P2KB-CORRECTION-FINDINGS.md`** (with IDs).
- **Gap ledger + questions-for-experts updated in `KNOWLEDGE-GAPS.md`** (answered rows moved, new raised, reviewer notes harvested, expert-only questions routed).
- Trust tier set in `AUTHORITATIVE-SOURCES.md`; lineage/supersession recorded in `DOCUMENT-LINEAGE.md` if an updated edition.
- Suggested next step (e.g. the YAML head working any routed conflicts; or central-repository-build integration).

This skill does NOT commit/push and does NOT edit P2KB YAML. It produces the
verified source extraction + the routed findings.

## 8. Process-improvement note — what this skill supersedes

This skill was authored when better tooling existed than the methodology docs
assume. **Update these docs in the same pass that this skill is used** (do not
defer):

- `methodology/source-code-extraction-methodology.md` — its "PDF-First /
  DOCX→request human intervention" rule was a tooling-era workaround. Replace
  with the **validator-driven** rule (§2): DOCX-primary, `pnut_ts`-gated, PDF
  as per-example fallback.
- `methodology/image-extraction-methodology.md` v3.0 — its PyMuPDF +
  brightness + coordinate-rescue pipeline is largely superseded by **DOCX-media
  + `image-tools-mcp`** (§3). Keep coordinate-rescue documented as the fallback
  for assets not embedded in the DOCX.

We actively improve our processes whenever we see the opportunity — capturing
that improvement here, and in the source docs, is part of finishing the work.

## What NOT to do

- **Don't overwrite a prior edition's source folder** — a new edition is a new `sources/<src>/`; keep lineage.
- **Don't edit `deliverables/ai/P2/` YAML** — route content conflicts to the corrections register; the YAML head applies them.
- **Don't single-source a verification** — use every eligible source (§4); a lone citation is not corroboration.
- **Don't treat "PDF-first for code" / "PyMuPDF for images" as laws** — they are fallbacks now (§2, §3).
- **Don't skip `pnut_ts` validation of extracted code** (use `-d` for DEBUG code), or ship a code example that did not compile clean.
- **Don't mark a source complete with open gates** — completeness % and gate status on the dashboard are load-bearing for `whats-next` resume.
- **Don't bury a conflict** — inter-source disagreement is an outcome to surface, not smooth over.
