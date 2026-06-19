# Streamer Programming Guide — Grounding-Audit Fix Plan (2026-06-19)

**Head:** manual production → `manual:p2-streamer-programming-guide`
**Source audit:** `engineering/document-production/manuals/p2-streamer-programming-guide/audit/streamer-grounding-audit-2026-06-19.md`
**Master to edit:** `opus-master/streamer-body.md` (1617 lines / 67 KB → Sacred Rule #1 backup required)
**Current version:** v1.0.0 — **RELEASED 2026-06-10** (`deliverables/documents/DOCs/P2-Streamer-Programming-Guide.pdf` + published changelog). This cycle ships **v1.0.1** as a `release-manual` *update* of the public doc.
**Discipline:** `document-finalize` (gather done; this is cluster → order → batch → render-once)

---

## Finding inventory (closed by the audit — clustered)

| Cluster | Findings | Head | Severity |
|---------|----------|------|----------|
| **1. Code-compile sweep** | H-1 (colon labels, 11 sites/8 blocks), L-1 (reserved-word labels `field`/`y`), H-2 (`wrlut()` as Spin2), H-3 (`clkfreq` as PASM2 operand ×2), L-11 (akpin order) | manual | HIGH |
| **2. Pin/DAC table transposition** | H-4 (§6.2, §8.1 self-contradicting), M-1 (§5.2, §13.1, App A) | manual | HIGH/MED |
| **3. Semantics** | M-2 (XRL event-clear), M-3 (WXPIN comment), M-4 (WAITXFI wording), M-5 (Goertzel −4..+4) | manual | MED |
| **4. LOW/INFO polish** | L-2…L-10 (9 items) | manual | LOW |
| **5. KB drift (route + fix at YAML head)** | DRIFT-1 (streamer-symbols.yaml desc), DRIFT-2 (pin-selection.yaml %101), DRIFT-3 (dds-goertzel.yaml range), DRIFT-4 (verify setxfrq.yaml) | yaml | — |

**De-dup notes:** H-4 and M-1 are the *same* defect (one rewrite); DRIFT-1 is its root cause. M-5 and DRIFT-3 are the same fact in two heads. L-3/L-4 live inside the §15.1 VGA code block touched by Cluster 1.

---

## Trust-chain grounding for the table fix (Cluster 2)

Silicon Doc v35 `part2-pixel-ops.txt:182–209` is **primary** and outranks the derived YAML. The symbol token `<N>P_<M>DAC<B>` decodes as: **N = pin count**, **M = DAC channel count**, **B = DAC bits**. Example: `X_RFBYTE_8P_1DAC8` = 8 pins, 1 DAC channel, 8 DAC bits. The transposition error read M (the "1") as the pin count. The manual fix is grounded directly in Silicon, so it is **not blocked** on the YAML DRIFT-1 fix.

---

## Design decisions

### Decision A — DRIFT YAML edits: **DECIDED (b)** ✅
Stephen confirmed: log DRIFT-1..4 as **F-154…F-157** now, fix the manual now grounded directly in Silicon, do the YAML edits in the next yaml-head sweep (v1.10.1).

### Decision B — Canonical pin/DAC table column scheme — **PENDING confirm**
Not an invention: Silicon `part2-pixel-ops.txt` presents each row as `<N>-pin + <M>-DAC<B>` (e.g. `RFBYTE -> 8-pin + 1-DAC8`). The manual's current §6.2/§8.1 tables show only two numeric columns and (a) mislabel the **DAC-channel count** as "Pins" and (b) **omit the true pin count entirely**. Fix = column-ize Silicon's own decode and restore the dropped pin count:
- **Proposed (3 columns):** `Mode | Symbol | Hub Read | Pins | DAC Ch | DAC Bits`
- Corrected row, every value read off Silicon: `%1010 | X_RFBYTE_8P_1DAC8 | RFBYTE | 8 | 1 | 8`

### Decision D — Two judgment-call LOW items: **DECIDED (my choices)** ✅
- **L-6** (§15.1 OBEX #2847 technique UNVERIFIED): soften to cite the driver for the *general approach* only.
- **L-7** (§13.4 SPI uses 4-pin mode for byte-out): switch to the 1-pin `X_RFBYTE_1P_1DAC1` (§11.3's mode).

### Decision C — code-example fixes (clarified)
Each broken example is fixed to be **correct, idiomatic, and compile-clean under `pnut-ts -d`**, changing only what the defect requires (no gratuitous redesign of sound teaching code — document-finalize's no-"while-I'm-here" rule, which also avoids injecting new errors into a released manual). Real restructures are done in full where correctness needs them: `wrlut(t,i)` → inline PASM; `clkfreq` operand → `rdlong clkf,#$44` then `qfrac`.

### Decision E — release path (corrected; manual is already public)
v1.0.1 is a `release-manual` **update** of the public doc: make all edits → **one** PDF Forge render → verify PDF → promote v1.0.1 to deliverables → update published changelog + README index → surface commit/tag/push. **OPEN:** whether the previously-deferred visual review (diagrams, emoji glyphs, 7 TikZ figs, 3 Tier-3 candidates) folds into v1.0.1 or stays a separate cycle — pending Stephen.

---

## Execution order (rework-safe; render ONCE at the end)

0. **Backup** `streamer-body.md` to a timestamped copy *outside* opus-master (e.g. `NO-COMMIT/`), delete after verification — git is the real record; do NOT leave a sibling `.backup` that could become a poison master (`reference_desilva_masters_current_source`).
1. **Route DRIFT-1..4 → F-154…F-157** in `engineering/operations/P2KB-CORRECTION-FINDINGS.md` (no-deferring satisfied by routing to the active v1.10.1 sweep). *(per Decision A=b)*
2. **Lock the column scheme** *(Decision B)* — no table edits until confirmed.
3. **Batch 1 — Code syntax sweep:** strip trailing-colon labels doc-wide (H-1), rename reserved-word labels `field`→`vfield`/`y`→`ycnt` (L-1), wrlut→inline PASM (H-2), clkfreq→rdlong (H-3 ×2), reorder akpin (L-11), fix L-2 handshake + L-3/L-4 VGA constants inside the §15.1 block. **Recompile EVERY code block with `pnut-ts -d` to green** (`feedback_compile_debug_code_with_d_flag`).
4. **Batch 2 — Pin/DAC rewrite (H-4 + M-1):** one consistent pass across §5.2/§6.2/§8.1/§13.1/App A using the confirmed scheme + Silicon counts.
5. **Batch 3 — Semantics (M-2…M-5):** XRL event-clear qualifier, WXPIN comment, WAITXFI wording, Goertzel −4..+4.
6. **Batch 4 — LOW/INFO (L-5, L-8, L-9, L-10 + L-6/L-7 per Decision D).**
7. **Verify** the full inventory against the edited master; confirm every code block compiles green.
8. **prepare-manual → stage to Forge → Stephen renders ONCE → verify PDF** (page count / outline / spot-check the fixed tables & code), bump CHANGELOG to v1.0.1.

---

## Progress log

- **2026-06-19 — Step 0/1 DONE:** master backed up; F-154…F-158 logged.
- **Batch 1 (code sweep) DONE + COMPILE-VERIFIED:** 11 colon-labels stripped;
  `field`→`vfield` (audit was wrong that `y` is reserved — `y` compiles, kept);
  4 `...` elisions → register-build (`mov`/`add`); `wrlut()`→`sine_table[i] := t`;
  `clkfreq`→`rdlong clkf,#$44` (×2); akpin reorder (L-11); hub-flag clear (L-2);
  WXPIN comment (M-3); 25.175 MHz `$0CE3_BCD3` (L-3); L-4 placeholder comment.
  Every edited block compiles `pnut-ts -d`; all lines ≤ K=76.
- **L-7 RESOLVED with a reversal of Decision D:** Silicon shows `X_IMM_8X4_1DAC4`
  is a **4-pin** mode (audit was right); the KB's `selection_guide.spi_output`
  *and* the manual both inherited it wrong. Fixed the manual's SPI examples
  (§13, §16.1) → **`X_IMM_32X1_1DAC1`** (the 1-pin immediate mode, Silicon-grounded,
  count = bits) — NOT the audit's RFBYTE suggestion, because §16.1 uses immediate
  data. KB drift logged **F-158**.
- **Batch 2 (pin/DAC tables) DONE + SILICON-VERIFIED:** rewrote all five locations
  (§5.2, §6.2, §8.1, §13.1, Appendix A) to true Pins (N) + DAC Channels (M) + DAC Bits
  (B) per Silicon `part2-pixel-ops.txt:145–209` (token `<N>P_<M>DAC<B>`; for IMM
  Pins=W of `<S>X<W>`). §5.2 gained DAC Bits col + corrected Pins/DAC-Ch; §6.2 gained
  DAC Channels col + true Pins; §8.1 gained DAC Channels col + true Pins; §13.1 IMM
  descs fixed (1DAC2→2-pin, 8X4 all 4-pin); App A IMM/RDFAST/WFBYTE description column
  uniformly reset to Silicon `<N>-pin + <M>-DAC<B>` form (caught more transposed rows
  than the audit's 11 — every IMM/WFBYTE row hand-verified). Also fixed the §5.2
  example (was "8 bytes to 1 pin" / count 8 → "4 bytes to an 8-pin group" / count 4;
  recompiled green `pnut-ts -d`). Every value re-checked against Silicon.
- **Batch 3 (semantics) DONE:** M-2 §14.3 rewritten — XINIT/XCONT/XZERO re-arm
  EVENT_XMT/XFI/XRO (10/11/12) only; **EVENT_XRL (13)** clears on cog start / its own
  poll-wait-jump (verified vs Silicon `part3-interrupts.txt` L85-100 "established by"
  column). M-4 §16.2 reworded — WAITXFI blocks only for streamer finish, no smart-pin
  clock knowledge (check TESTP separately); matches the section's own pitfall + `waitxfi.yaml`.
  **M-5 WITHDRAWN — audit finding INVERTED:** Silicon (`part2-more-content.txt` L227-228 =
  `p2-documentation.txt` L4094-95) says the bitstream sum is "an integer **from -3 to +3**";
  even channel-counts are shifted right one bit (L177-179), so max magnitude = 3. The manual's
  "−3 to +3" is CORRECT — **no §10.2 edit.** Register **F-156 reset to RESOLVED-INVALID**;
  DRIFT-3 withdrawn; audit M-5/DRIFT-3 entries annotated. (Hand-verify caught the audit error
  per `feedback_handverify_audit_findings`.)
- **Batch 4 (LOW prose) DONE:** L-5 §16 intro ("stay locked together" → "both driven
  from the same system clock, matched rates" — consistent with M-4); L-6 §15.1 OBEX
  #2847 ("Verified against…" specific-technique claim → "worked reference using this
  general approach", per Decision D); L-8 §7.3 example header now states "(assumes
  250 MHz sysclk)"; L-9 SINC framing unified on the **D[23]** selector (§10.1 note added;
  §13.1 SINC2 value `$87<<16` → `7<<16 + 1<<23` to expose D[23]; App A already explicit
  — verified `7<<16 + 1<<23 = $F087_0000`); L-10 §4.2 footnote added explaining the
  `%1111_x111` row mixes mode nibble D[31:28] + config D[19:16]=%x111 with D[23]=SINC.
- **CONTENT CYCLE COMPLETE — full inventory resolved:** H-1/2/3/4, M-1/2/3/4 fixed;
  M-5 withdrawn (audit inversion); L-1…L-11 all fixed or resolved. Code-line-length
  audit GREEN (K=76); §5.2 example recompiled green `pnut-ts -d`.
- **CALLOUT MIGRATION DONE (Stephen-approved, folded into v1.0.1):** the inline emoji
  markers (⚠️/💡/🔧) were being **dropped** by XeLaTeX (not boxing — vanishing). The
  IOSP/PASM2 family already migrated off emoji onto platform fenced callouts; the streamer
  never got it. Converted all 17 body callouts → `::: caution` (7), `::: tip` (5),
  `::: hardware` (5), plus reworded the front-matter legend to the CAUTION/TIP/HARDWARE
  boxes. **Platform change (shared, additive):** added `HardwareBlock` (graphite) to
  `platform/templates/p2kb-platform-content.sty` + `::: hardware` branch in
  `platform/filters/p2kb-platform-code-coloring.lua` (Tip/Caution blocks already existed).
  Both platform files staged; `manual_store_platform_hashes` updated; PLATFORM ledger
  lines appended (PUBLICATION-ROSTER.md, hash reconciled at commit).
- **v1.0.1 BUNDLE STAGED** in `outbound/p2-streamer-programming-guide/`: refreshed `.md`
  (cover→v1.0.1), `request.json` (doc-switch force-stage + v1.0.1 metadata),
  `p2kb-platform-content.sty`, `p2kb-platform-code-coloring.lua`.
- **NEXT:** Stephen renders ONCE → verify PDF (callout boxes render w/ correct title
  bars + colors — esp. new HARDWARE graphite; NO emoji/tofu; spot-check fixed tables
  §5.2/§6.2/§8.1/App A + §10.1/§14.3) → bump CHANGELOG to v1.0.1 → release-manual update
  → commit (reconcile PLATFORM ledger hashes).

## What is NOT in this cycle (named carve-outs)
- The actual YAML DRIFT edits → folded into the parked yaml-head **v1.10.1** sweep (Decision A=b).
- The deferred **visual/render review** (diagrams, emoji glyphs) and **deliverables promotion** → after this content cycle (per `project_streamer_manual_next`).
