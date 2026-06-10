# Spin2 v55 Documentation — Complete Extraction Audit

**Source:** Parallax Spin2 Language Documentation **v55** (dated 2026-05-07)
**Files:** `Parallax Spin2 Documentation v55.docx` (6.7 MB, primary) · `…- Google Docs.pdf` (58 pp, reference)
**Authority:** 🏆 AUTHORITATIVE — and the **matched-compiler edition** (pnut-ts `v1.55.0` is ratified against PNut v55, so this spec text matches our ground-truth compiler).
**Ingested:** 2026-06-10 via the `ingest-source` skill (first run).
**Type:** **Delta / update ingestion** over the prior baseline **v51a** (the doc's v51, 2025-04-02). Delta = editions **v52 → v55**.

---

## Extraction results

| Pass | Result |
|------|--------|
| **1 — Content** | `spin2-v55-text.txt` — 204,468 chars / 1,740 lines, tables preserved as pipe-delimited rows (DOCX literal-char stream; no column-bleed). |
| **2 — Code examples** | `assets/code-20260610/` — 952 monospace blocks; **169 substantial (≥3-line)** written; **29 compile clean** under pnut-ts v1.55.0; remainder are illustrative *fragments* (partial DAT/VAR/PUB needing object context, version-gated struct snippets missing directives) + a few prose blocks mis-swept by font detection. **Whitespace fidelity confirmed faithful from DOCX.** |
| **3 — Images** | `assets/images-spin2_lang_ref_v55-20260610/` (24 PNG/GIF) + `image-catalog.md` — lossless from DOCX `word/media/`; **0 black/failed extractions**; each mapped to its doc heading/caption. Figures are DEBUG-display screenshots + FIELD-POINTERS diagrams. |
| **6 — Cross-source conflict audit** | 7 delta features boundary-probed vs pnut-ts v1.55.0. See below. |

## Code-fidelity note — `...` line-continuation (verified, no loss)

`...` (three ASCII periods) is a Spin2 **line-continuation** marker (added v37: "ignore rest of line, continue parsing on the next"). Word/Docs auto-correct can fold a literal `...` into `…` (U+2026), which the compiler rejects (`Unrecognized character $2026`). **Checked for v55:** all real `...` continuations survived intact as ASCII (15×); all 11 `…` (U+2026) are genuine **prose elision** (none at a code line-end) → **no code example was missed or broken.** Rule now encoded in the `ingest-source` skill (normalize auto-correct substitutions; validate-then-filter prose noise).

## Conflict-audit outcome (delta = the whole value — features were already in the KB → no gap-fill)

| Feature | Edition | Verified gate | Verdict |
|---------|---------|---------------|---------|
| `ENDIANL(long)` | v52 | `{Spin2_v52}` (enforced) | ✅ correct in `endianl.yaml` |
| `ENDIANW(word)` | v52 | `{Spin2_v52}` (enforced) | ✅ correct in `endianw.yaml` |
| `OFFSETOF(struct.member)` | v53 | `{Spin2_v53}` (enforced) | ✅ correct in `offsetof.yaml` |
| struct bitfields | v54 | `{Spin2_v45}` enforced (`v54` = intent) | ✅ correct in `struct-bitfields.yaml` |
| `MOVBYTS(long, pattern)` | v52 | **none** (NOT enforced) | ⚠️ **F-100** — gating field ambiguous |
| `DEBUG_END_SESSION` | v52 | `{Spin2_v52}` | ❌ **F-099** — fabricated runtime behavior |
| `NEXT`/`QUIT` level | v52 | **none** (NOT enforced) | ❌ **F-098** — `NEXTN`/`QUITN` fabricated; range 1-16→**1-15**; semantics inverted (5 files) |

**Key lesson:** "introduced in edition vNN" ≠ "enforced `{Spin2_vNN}` gate." Three features (MOVBYTS, NEXT/QUIT level, struct-bitfields-v54) carry an edition-of-introduction label that is **not** a compiler-enforced gate — the boundary-probe must distinguish the two. Findings routed to `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (F-098..F-100) for the YAML head.

## Completeness / gates

- ✅ Content extracted (text + tables)
- ✅ Code extracted + compiler-validated (continuation hazard cleared)
- ✅ Images extracted + cataloged (0 failures)
- ✅ Delta conflict audit complete; gates compiler-verified; conflicts routed
- ⬜ Gap-fill: **none required** (all v52–v55 features already present in KB)
- ➡️ Supersession: v55 becomes the authoritative Spin2-language edition over v51a (see `DOCUMENT-LINEAGE.md`).

**Completeness: 100% for the delta scope** (the prior v51a full extraction stands; this pass adds the v52–v55 reconciliation + the matched-compiler authority).

## Cross-Source Q&A ledger (pass 6 — all three legs)

Per the corpus-accumulation model: each ingested source *answers* some prior open questions and *opens* new ones. v55's effect on the corpus-wide knowledge state:

### Questions ANSWERED (prior holes v55 closes)
- **"Complete operator precedence table (16 levels)"** (`gaps-consolidated.md #7`) → **CLOSED.** v55 carries the full structured precedence spec — Var-Prefix/Var-Postfix/Address/Unary/Binary/Ternary/Assign sub-tables with Term-Priority & Assign-Priority columns (`spin2-v55-text.txt:409-494`).
- **"All floating-point operators"** (`#7`) → **CLOSED.** Full ladder present (`POW LOG2 EXP2 LOG10 EXP10 FSQRT FABS ROUND TRUNC`) with a dedicated Floating-Point-Operator column. (`gaps-consolidated.md` annotated; Spin2-language coverage 70%→85%.)
- **Field pointers** (`^@variable` / `FIELD[ptr]`) — v55 has a dedicated section (`:871-875`) + the `^@` precedence-table row (`:422`); strong material to confirm KB coverage against.

### Questions RAISED (new holes v55 opens)
1. **Does `pnut-term` (the DEBUG host) implement the `DEBUG_END_SESSION` runtime?** The compiler is verified (recognizes/gates/value-27); the side-effects (close DEBUG.LOG, close PNut `-rd`, P2 continues) live in the terminal host — unverified, and the AI-dev loop depends on them.
2. **KB-wide edition-vs-enforced-gate sweep.** The v55 audit found 3 entries treating an "introduced-in-vNN" label as an enforced gate (F-098/F-100 + the MOVBYTS class). How many *other* KB YAMLs carry `minimum_version`/`introduced_in` labels that need a boundary-probe to confirm whether the gate is actually enforced?
3. **Is the AI-assisted-development DEBUG workflow captured?** v55 documents a whole loop (`DEBUG_END_SESSION` + DEBUG.LOG + `PNut -rd`) — a new usage-pattern coverage area for the KB/manuals.

### Conflicts (leg 1 — done in the delta audit)
3 routed to the corrections register (F-098/099/100); 4 features confirmed correct. See above.
