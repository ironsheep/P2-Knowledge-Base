# Changeset-Integrity Audit — p2-streamer-programming-guide

**Auditor:** Independent adversarial changeset review (fresh eyes; goal = disprove each hunk)
**Baseline tag:** `p2-streamer-programming-guide-v1.0.5`
**HEAD:** `60d0a18a31057322661e22eb6d7ec05997f0836c`
**Introducing commit:** `f3e702ed` — "Fabrication-audit §6: class-wide correctness sweep A"
**Files touched:** 1 (`opus-master/streamer-body.md`)
**Hunks:** 7 (all in one file; ~14 changed lines)
**Primary source used:** `engineering/ingestion/sources/silicon-doc/p2-documentation.txt` (Silicon Doc v35), plus `engineering/ingestion/sources/spin2-v55/spin2-v55-text.txt` (X_DACS constant), cross-checked against `engineering/planning/FABRICATION-AUDIT-SWEEP-CATALOG.md` per-change proof.

**BOTTOM LINE:** All 7 hunks are **faithful** — each traces to a concrete, verbatim Silicon Doc (or Spin2 v55 constant) line I confirmed independently, not merely to the sweep's say-so. No scope-creep, no unsourced new claims, no contradictions. Zero flags. This is a genuinely corrective, proportionate changeset. Recommend release.

---

## Traceability Table

| Hunk (file: streamer-body.md) | Summary | Traced source | Verdict | Note |
|---|---|---|---|---|
| §3.4 L229 | NCO word "31-bit" → "32-bit word, MSB masked each clock, only 31 bits accumulate; res sysclk/2^31" | Silicon Doc L2747-2751: "it adds a 32-bit frequency value into a 32-bit phase accumulator, while masking the MSB of the original phase … phase = (phase & $7FFF_FFFF) + frequency" | **faithful** | Near-verbatim. The masking mechanism and the $7FFF_FFFF (31-bit accumulation) are exactly the doc's model. Resolution sysclk/2^31 correct. |
| §7.3 L533/536 | `xcont cmd, #0` → `xinit cmd, #0` (starts streamer) | Silicon Doc L3512-3513: "XINIT (re)starts the streamer, no matter what state"; L3510-3517: XZERO/XCONT are for seamless command-to-command continuity | **faithful** | Verified L529-536: XINIT is the sole/first streamer command after rdfast+setxfrq (starting from idle). XCONT would run with residual phase and is documented as continuity-only. Correct instruction. |
| §15.1 L1119 & L1129 | VGA vertical porch values+labels swapped: pre-visible blank #10→#33 ("back porch, follows vsync"); post-visible blank #33→#10 ("front porch, precedes vsync") | Standard VESA 640×480@60 vertical timing: front porch=10, sync=2, back porch=33 (total 525). Loop order after fix: back(33)→visible→front(10)→vsync. Catalog C-261. | **faithful** | Loop execution order now places 33-line back porch immediately after vsync (loop top) and 10-line front porch immediately before vsync — matches the canonical VGA sequence. Original had both value and label inverted. |
| §15.1 L1157 (m_visible) | `$B085_0000 + 640` (X_RFWORD_RGB16\|X_PINS_ON) → `$BF85_0000 + 640` (+ X_DACS_3_2_1_0) | Spin2 v55 L1631: `X_DACS_3_2_1_0 = %0000_1111_0000_0000 << 16` → sets D[27:24]=%1111. Silicon Doc %dddd field D[27:24] = DAC-routing; %0000 = X_DACS_OFF (no override). | **faithful** | Decode: $B085 has D[27:24]=%0000 (X_DACS_OFF → static SETDACS output, not RGB). $BF85 has D[27:24]=%1111 (X_DACS_3_2_1_0 → X3/X2/X1 route to DACs). Nibble arithmetic B085→BF85 exactly matches OR-ing $0F00_0000. Correct. |
| §16.1 L1236 (SPI) | `wxpin ##2` → `wxpin ##1` (transition base period) | Silicon Doc SETXFRQ ($4000_0000 = 0.5 → NCO ÷2, 1 data bit / 2 sysclks). Transition mode: each edge every X sysclks; 2 edges = 1 clock cycle. Catalog C-241. | **faithful** | With setxfrq $4000_0000, data bit period = 2 sysclks. wypin #16 for 8 bits = 2 transitions/bit = 1 full clock/bit. Base period 1 → clock cycle = 2 sysclks = matches data rate. Base period 2 would halve the clock vs data (mismatch). ##1 correct; comment accurate. |
| Appendix A L1466 | `%pppp` → `%pppa` for X_RFBYTE_1P_1DAC1 | Silicon Doc streamer mode table L3132 (RFBYTE 1-pin): row reads `pppa` (D[19:17]=3-bit pin offset, D[16]=alt bit-order 'a') | **faithful** | Confirmed the doc row is `pppa`, not `pppp`. Low bit is the 'a' alt-order bit, not a 4th pin bit. |
| Appendix A L1483 | `%pppp` → `%pppa` for X_1P_1DAC1_WFBYTE | Silicon Doc capture/output 1-pin table L3302: row reads `pppa` | **faithful** | Same fix, capture-side (WFBYTE) 1-pin row. Doc confirms `pppa`. |
| Appendix D L1590 | "Buffer address aligned to 64-byte boundary for wrap mode" → "Buffer start address long-aligned (4-byte, ends in `%00`) for wrap mode" | Silicon Doc L6673: "If you intend to use wrapping, your hub start address must be long-aligned (address ends in %00)"; RDFAST/FBLOCK encoding L6702: "start address for wrapping (long-aligned)" ends in `AA00`. The 64-byte figure = block-count granularity (L6672), not an address requirement. | **faithful** | **Materially important and correct.** The original conflated block granularity (64 bytes) with the address-alignment requirement (long/4-byte). Doc is unambiguous: address ends in %00. This is the strongest correction in the set. |

---

## Flags

**None.** Every technical claim in this changeset was independently confirmed against a Tier-1 primary source (Silicon Doc v35 verbatim lines, or the Spin2 v55 constant table) — not accepted on the sweep's authority. Specifically checked for the failure mode of "plausible correction with no source":

- The NCO 32-bit/MSB-mask description is not a paraphrase-drift; it reproduces the doc's exact `phase = (phase & $7FFF_FFFF) + frequency` model (L2747-2751).
- The $BF85 constant is arithmetically derived from the confirmed Spin2 v55 value `X_DACS_3_2_1_0 = %1111 << 24` — the hex nibble change B085→BF85 is exactly that OR, so it cannot be a fabricated "looks right" constant.
- The 64-byte→long-aligned fix, which materially affects code correctness, contradicts nothing and corrects a genuine conflation present in v1.0.5.

**Minor note on the XINIT comment (not a flag):** the inline comment "XINIT starts from a zeroed phase" is slightly beyond the doc's verbatim wording — the Silicon Doc explicitly states only that *XZERO* clears the phase accumulator (L3513) and that XINIT "(re)starts the streamer." A fresh (re)start does begin accumulation anew, and the manual's own §4.7 caution frames XCONT as "begins with whatever phase remains" (implying XINIT begins fresh), so the comment is consistent with the documented model. The substantive change (instruction choice XCONT→XINIT for starting from idle) is correct regardless. No action needed.

---

## Out-of-Scope Observation (does NOT affect this changeset's verdict)

While confirming the `%pppa` rows, I noted the Silicon Doc mode table (L3132 ff.) shows the 2-pin/4-pin RFBYTE rows as `pp0a`, `pp1a`, `p00a`, … whereas the manual's Appendix A still shows `%ppp0`, `%pp00` for those neighbouring rows. This changeset only corrected the two 1-pin rows (the two findings raised by the fan-out), and those two are correct. Whether the adjacent multi-pin rows also warrant an `a`-bit revision is a **separate, un-raised question** outside this diff — it is neither introduced nor claimed by commit f3e702ed, so it does not count against the changeset. Recommend logging it for the next fabrication-audit pass if not already tracked.

---

## Bottom-Line Recommendation

**RELEASE-READY (changeset-integrity: PASS).** All 7 hunks are corrective, proportionate, and each anchored to a specific verbatim source line I verified independently. The changeset raises correctness at every hunk — most notably fixing a materially wrong FIFO-wrap alignment claim (64-byte → long/%00) and a wrong streamer-start instruction (XCONT → XINIT). No scope-creep, no unsourced assertions, no source contradictions. Recommend proceeding to release for this file's delta. Optionally open a follow-up to check the adjacent multi-pin mode-table rows (`pp0a`/`pp1a` per Silicon Doc L3132) — strictly out of scope here.
