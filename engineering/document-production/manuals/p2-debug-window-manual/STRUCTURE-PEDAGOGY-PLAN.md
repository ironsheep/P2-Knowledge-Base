# Structure & Pedagogy Plan — Debug Window Manual

**Purpose.** Evaluate the current manual's learning arc against the creation-guide's
teaching intent and the voice guide's reference model, decide where each salvaged
pattern belongs, and reconcile the guides — before any clean-room content is written.

**Inputs studied:** `voice-guide.md` (authoritative reference voice, adopted 2026-05-31),
`creation-guide.md` (learning philosophy + chapter template; voice section + outline now
stale), the current `opus-master/` source, and the legacy coverage audit.

---

## 1. Current state — the manual is already well-structured and in-voice

Reading the current source closely (not the audit summaries) changes the picture:

- **`ch01-foundation`** already delivers the orientation value the legacy "iceberg" chapter
  aimed at — a nine-window "pick by the shape of your data" table, the create-by-name /
  feed-by-name model, the **values-vs-command-codes** rule, common commands, and the
  single-step-debugger boundary — in the authoritative voice. No iceberg, no marketing.
- **`ch02-getting-started`** is a clean onboarding loop: tools, `-d`, first window, the
  no-hardware philosophy, config symbols.
- **`ch14-multiwindow-pasm`** is **v55-correct** where the legacy was fabricated: it
  explicitly states there is *no* cross-window coordination (`no TIMESTAMP / OVERLAY /
  SYNC_GROUP / TRIGGER EXTERNAL / broadcast`) and covers PASM `DEBUG` (DAT, inline, pointer
  differences, ISR caution) thoroughly.

**Conclusion:** the v3 rewrite is sound. The job is **targeted enrichment with worked
examples**, not restructuring.

## 2. Learning arc & ordering — sound, keep it

```
Part I  Foundation     ch01 model → ch02 setup
Part II The Windows     ch03 TERM → ch04 BITMAP → ch05 PLOT → ch06 LOGIC →
                        ch07 SCOPE → ch08 SCOPE_XY → ch09 FFT → ch10 SPECTRO → ch11 MIDI
Part III Integration    ch12 Bidirectional → ch13 Packed Data → ch14 Multi-window + PASM
Part IV Appendices      A command ref · B packed formats · C color/coordinate
```

This is a defensible simple→complex progression: text → raster → vector → digital → analog
time → analog XY → frequency → spectrogram → special. TERM-first is correct (it exercises the
whole feed model). **Recommendation: keep the ordering as-is.**

## 3. Per-window chapter template (voice guide §2.2) — apply consistently

Each window chapter should present, in order: (1) what it shows; (2) creation/config command +
**all** parameters; (3) per-update data commands; (4) control/feature commands; (5) one
complete `pnut_ts`-compilable example; (6) "when to use" + considerations + cross-refs. The
salvaged worked examples slot into (5)/(6) — they do **not** need new chapters.

## 4. Revised salvage scope — the honest narrowing

The coverage audit over-counted: it flagged already-covered material and fabricated content as
"merge." Re-assessed against the actual current chapters and the voice guide:

| Legacy candidate | Re-assessment | Action |
|---|---|---|
| ch01 vision-gap ("Debug Iceberg") | Value already served by `ch01-foundation`; iceberg/marketing **forbidden** by voice guide | **Drop.** Optionally add a short "which window for which problem" task-index if you want one (voice guide §1.1 invites it). |
| ch02 terminal-mastery (GOTOXY dashboards, menus, bar-graphs) | `ch03-term` documents the control codes but lacks **worked dashboard/menu patterns** | **Salvage — real.** Add 1–2 in-voice worked examples to `ch03-term` §example/use-cases. |
| ch04 layer-composition (layer/sprite technique; "20×") | `ch05-plot` has the syntax; the **low-flicker layer/sprite *technique*** as a worked example is thin. "20×" is forbidden. | **Salvage — narrow.** One worked layer/sprite update example in `ch05-plot`; no performance claim. |
| ch06 professional-instruments (gauge, LED panel, VU, switches) | `ch05-plot` has primitives but **no built-instrument worked examples** | **Salvage — real (highest value).** Add 2–3 software-only instrument examples (gauge w/ CORDIC needle, LED/VU panel) to `ch05-plot`. |
| ch12 multi-window (orchestration, sync, bandwidth mgr) | Mostly the cross-window-coordination **fabrication** `ch14` correctly debunks; real value (POS layout, loop feeding) already covered | **Drop.** |
| ch13 pasm-integration (cycle-accurate, FIFO, profiling) | PASM `DEBUG` already covered in `ch14`; profiling/timing depth mostly unverified | **Drop** (optionally: one verifiable `GETCT` timing-of-a-code-section example in ch14 if desired). |
| ch14 production-workflows (screenshot/CI/test) | `SAVE`→`.bmp` already noted; CI/test framing is aspirational, not window behavior | **Mostly drop.** Optionally one "using `SAVE` to capture a window for docs" use-case note. |

**Net:** the genuine clean-room work is **three enrichment passes** — worked TERM dashboard
patterns (ch03), worked PLOT instrument examples (ch05), and one PLOT layer/sprite technique
example (ch05) — plus small optional notes. This is far less than the original 7-chapter list,
and it keeps the manual lean and in-voice rather than re-bloating it.

## 5. Placement map (the real work)

| # | Pattern (re-authored from v55 bibles, `pnut_ts`-validated, reference voice, software-only) | Lands in |
|---|---|---|
| A | TERM dashboard: cursor-positioned multi-field status panel updated in place | `ch03-term` worked example / use-cases |
| B | TERM menu / bar-graph pattern (optional, if it adds beyond A) | `ch03-term` use-cases |
| C | PLOT analog gauge — CORDIC-driven needle on a scale | `ch05-plot` worked example |
| D | PLOT LED / VU-style panel (boxes lit by value) | `ch05-plot` worked example |
| E | PLOT layer/sprite low-flicker update technique | `ch05-plot` use-cases |
| (opt) | TERM task-index "which window for which problem" | `ch01-foundation` or front matter |
| (opt) | `SAVE`-for-documentation note | `ch14` considerations |

## 6. Creation-guide reconciliation (fold-in, per your request)

The creation-guide is partly stale and should be brought into agreement with reality:
- **Voice section** ("Discovery Guide" / "exploratory excitement" / "Look at that!") — superseded
  by `voice-guide.md` (authoritative reference, no celebration). Replace with a pointer to the
  voice guide.
- **PART 3 chapter outline** still lists the legacy 14-chapter narrative structure (vision-gap,
  layer-composition, professional-instruments, …) — replace with the current window-reference
  outline (the §2 arc above).
- **Source-grounding** references to "PNut v51a" → "PNut v55" (matches the re-grounded bibles).
- Keep intact: the No-Handwaving principle, claim-verification protocol, minimal-hardware
  philosophy, and the audit methodology — those are current and valuable.

## 7. Proposed execution order

1. **(this doc)** — agree the revised scope.
2. Reconcile `creation-guide.md` (§6 edits).
3. Clean-room enrichment passes, one at a time for review: **A/B (ch03)** → **C/D/E (ch05)**.
4. Re-assemble, then PDF rebuild (your option B).
5. Source-zip deliverable (after PDF).

---

*Open question for review: confirm the revised salvage scope (drop ch01/12/13, mostly-drop 14;
keep ch02/04/06 as worked-example enrichment), and whether you want the two optional items
(task-index, SAVE-for-docs note).*
