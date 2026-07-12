# P2 Debug Window Manual — Dedicated Sprint Spec (split-out)

**Status:** HELD (Stephen 2026-07-12) — carved out of the fleet-release wave; resolved in its **own** sprint, not tonight.
**Do NOT edit the Debug Window Manual tonight.** Tonight = fleet release of the *other* manuals (see
`nextup_fleet_release_tonight`). This doc is the standing spec for the separate Debug sprint.

**Full evidence:** the coverage-tracked re-audit report
`engineering/document-production/manuals/p2-debug-window-manual/audit/release-gate-2026-07-12-COVERAGE.md`
(per-agent ledgers were in the session scratchpad; the report is the durable digest). YAML side = register **F-212**
(+ held F-207/F-208), rides the KB rail (`release-yamls`), not the manual PDF.

**Ground state (good news, per Stephen):** the example ZIP / examples-library is **done** — all examples run, corpus
identity GREEN 32/32, compile clean `pnut-ts -d`. The example corpus is NOT part of this sprint's open work.

---

## Stephen's certified guidance (2026-07-12) — the authority for the fixes below

1. **PLOT text operators (TEXTSTYLE / TEXTSIZE / TEXTANGLE):** the ref-doc effort **now clearly defines these fields and
   their correct values**. **The manual's PLOT chapter MUST align to the certified ref.**
   - ⚠️ **OPEN CONFLICT to resolve FIRST in this sprint:** this audit's PLOT agent found the manual (ch05:319-320) +
     plot.yaml already match **EF-031 hardware** (horiz %10=right/%11=left; vert %10=top/%11=bottom), while it read the
     ratified matrix §7.3 + PLOT ToO §8.2 as the *opposite*. **Resolution step:** confirm whether the **now-certified**
     ref values already equal EF-031. If YES → align manual to ref = no change (or a trivial one) and the "conflict" was a
     stale-ref artifact the certification already fixed. If NO → genuine ref-vs-hardware disagreement; empirical wins
     (trust chain), escalate. Do not assume; check the certified matrix/ToO values against EF-031 before editing.
2. **Window titles:** correct TITLE info now exists → **all window TITLE defaults must align.** Certified default caption =
   `"<name> - <TYPE>"` (`FormCreate:626`). Sweep every window chapter's directive table + Appendix A + the debug-displays
   YAMLs (F-212).
3. **POS / positioning — "cascaded" was never real.** Windows have a default position (PNut: top-left of host; PNut-ts: a
   default X/Y offset — *which is which is unconfirmed; nail down in the sprint*). **When no POS is given, windows
   auto-place.** The Debug Window Manual **intentionally omits POS** because auto-placement is a **toolset feature we want
   users to use** — the manual should teach "omit POS → the window auto-places" as the recommended path.
   - **Fix:** replace every "cascaded" default with the auto-placement description; keep the feature-forward "don't specify
     POS" guidance. **Do NOT write explicit POS pixel values.** The POS *overlap-vs-not* wording stays a hardware-hold
     (needs a multi-window PNut-ts capture) — do not flip the YAMLs.

---

## A. CERTIFIED-FIXABLE (apply in the Debug sprint — align manual to the certified ref / hardware / itself)

| # | Item | Location | Basis | Action |
|---|------|----------|-------|--------|
| A1 | PLOT `PRECISE` default inverted | ch05:161-176 | certified ToO: `vPrecise:=8` = whole-pixel default (sub-pixel OFF) | Rewrite: whole-pixel is the default; one `PRECISE` turns sub-pixel ON. |
| A2 | Window TITLE defaults | ch03/05/06/07/08/10/11 tables + Appendix A + F-212 yamls | certified `FormCreate:626` = `"<name> - <TYPE>"` | Sweep all to `<name> - <TYPE>`. |
| A3 | POS "cascaded" → auto-place (feature-forward) | ch03/06/07/08/10/11 | Stephen guidance #3 (no cascade; auto-place is the feature) | Replace "cascaded"; teach omit-POS→auto-place; NO pixel values. |
| A4 | PLOT text-operator fields align to certified ref | ch05 (TEXTSTYLE/TEXTSIZE/TEXTANGLE) | Stephen guidance #1 | **After** resolving the EF-031 conflict above, align manual to certified ref. |
| A5 | BITMAP SPARSE self-contradiction | ch04:49 vs ch04:320/398 | manual disagrees with ITSELF ("outline/grid" vs "round dot on background") | Fix line 49 to the round-dot-on-background model; exact word = hold (B-list). |
| A6 | BITMAP LUT "garbage" → "black `$000000` until LUTCOLORS" | ch04:86-87 | certified ToO zero-init (§14.1/§17.4) | Rewrite; verify against certified ToO. |
| A7 | SCOPE create-line channel-def | ch07:90-91 | **EF-003 hardware** (window does NOT appear, not "opens empty") | "opens with no channels" → "the window won't appear"; keep separate-message guidance. |

## B. CONTESTED — defer to the certification; verify at sprint, don't assume the audit's fresh re-read

These rest on a fresh fan-out re-read of the Pascal that may disagree with the bounded certification. **Trust the
certification unless a self-contradiction or hardware says otherwise.** Verify each against the CERTIFIED matrix/ToO;
change the manual only if the certified ref supports it.
- FFT `grid` 2-bit → 4-bit `%abcd` (ch09:132) — check the certified matrix §7.3 grid entry; align manual to it either way.
- SCOPE_XY "split a set across several feeds" (ch08:117) — rests on `ch:=0` method-local read; confirm vs certified ToO.
- FFT DOTSIZE "radius"→"diameter", RATE "samples"→"sample sets" — confirm vs certified ToO.
- LOGIC ch06 packed example feed-shape (ch06:180-188) — reconcile with ch13 (array feed = preferred, not mandatory).
- PC_MOUSE wire-vs-readout (ch12:138-140) — verify against certified matrix §4.4a/§4.4b before touching.
- Trigger-offset wording (SCOPE/LOGIC) — the MANUAL is already right per the audit; the disputed side is the REF (internal,
  non-shipping). No manual change; ignore for the deliverable.

## C. NEEDS-RESOLUTION (hardware-hold / raw-`.pas` — Stephen-gated, cannot close in-repo)
- **BITMAP SPARSE exact user-facing word** (round-dot-on-block vs ring/grid) — no BITMAP EF record; bench render.
- **POS exact origin pixels** + **POS overlap-vs-not** — multi-window PNut-ts capture; do not flip yamls meanwhile.
- **SET out-of-range clamp vs ignore** (ch04:241) — raw `.pas` `KeyValWithin` (assign-clamp or reject?). Not in the
  certification's bounded classes.
- **SCOPE `SAVE` filename required-vs-optional** + yaml `WINDOW` modifier — raw `.pas` `KeySave`.

## D. NOT manual work (internal / other rails)
- **REF matrix/ToO internal inconsistencies** (prose-vs-own-quoted-code: PLOT §6.1 origin, FFT MAG §2.3-vs-§11.4, LOGIC §6.5
  ALT example, SPECTRO §11 sign-label, matrix §6 CLOSE clause, etc.). The REF is an **internal grounding artifact, not a
  shipped deliverable** — these gate nothing. Optional cleanup pass only; NOT part of the manual release.
- **F-212 debug-displays YAML corrections** — KB rail (`yaml-knowledge-base-maintenance` + `release-yamls`), bundled with
  F-207/F-208. Separate from the manual PDF.

## E. Audit findings CONFIRMED as already-correct (no action — recorded so we don't re-chase)
- TERM default text color = Orange (uncontested; prior "Orange-vs-Lime hardware-hold" was an EF-025 misread — DROP).
- "Up to 32 display windows" = GROUNDED (Spin2 v55 text L1074). Not the LogicChannels=32 conflation.
- ALT packing = per-byte full within-byte reversal (manual CORRECT; verified `0x01→0x80`). Do NOT "fix" it.
- Packing unsigned-by-default (manual/appendix CORRECT; SPECTRO ToO sign-label is the stale artifact).
- Appendix A master table: no column transposition. Examples: all matrix-legal, byte-identical, F-207 anchor good.

---

## Sprint entry checklist (when we pick this up)
1. Resolve the **A4/EF-031** conflict first (certified ref vs hardware) — it gates the PLOT text-field alignment.
2. Apply A1-A7 (`document-finalize`), swept data-set-wide; leave B/C/D untouched.
3. File/confirm F-212 yaml drain on the KB rail.
4. Close C-items as Stephen's rig / raw-`.pas` access allows.
5. Re-audit at release depth against the (then-final) certified ref; `prepare-manual` → render → `release-manual`.
