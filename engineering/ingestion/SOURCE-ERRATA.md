# Source Errata — defects in the documents we ingest

> Backing doc **#5** of the ingestion set (README dashboard · `AUTHORITATIVE-SOURCES` ·
> `DOCUMENT-LINEAGE` · `KNOWLEDGE-GAPS` · **this**). Standing register, created 2026-08-25.
>
> **Next erratum ID: `E-008`** · **Next open-question ID: `D-002`**

## Why this is its own register

Three registers already exist and none of them fits a defect that lives in **someone else's
document**:

| Register | Answers | Disposition |
|---|---|---|
| `operations/P2KB-CORRECTION-FINDINGS.md` | what is wrong in **our** shipped KB | fix it here |
| `KNOWLEDGE-GAPS.md` | what **no source** tells us | fill it, or ask an expert |
| **this** | what a **source document** gets wrong | **report upstream; never silently "fix" the source** |

Filing a source erratum in the corrections register mis-states the work: there is nothing in our
tree to correct, and an agent reading it looks for a YAML edit that must not happen. Filing it as a
knowledge gap is worse — a gap says *we do not know*, while an erratum says *we know, and the
document is wrong*. Those are opposite states and they were being recorded in the same column.

**This register serves two purposes, and the second is the one that compounds.**

1. **Things we can clear up.** Each entry is drafted so it can be sent to Parallax as-is: what the
   document says verbatim, why it is wrong, and what the correct statement is, with evidence.
   Errata we report get fixed in the next edition, and every reader benefits — not just us.
2. **A map of where our understanding sits relative to our sources.** Every row records whether
   our KB **follows** the source, **diverges** from it, or **never carried it**. That map is the
   thing no single finding can give you: it shows, in one place, every point at which this project
   has knowingly departed from a Parallax document — and why it was entitled to.

The second purpose is why a row stays here after it is reported. A reported erratum is not a closed
one; it closes when a **new edition** of the document fixes it, and closing it is what triggers a
re-ingestion check.

## Precedent — this is a form Parallax already uses

Parallax publishes errata against its own manuals, and we have ingested one:
`sources/p1-propeller-manual-errata-v1.1/` (from `122-32000-Propeller-Manual-v1.1-Supp-Errata.pdf`).
So an erratum report is a document type they recognise and act on, not an unsolicited critique.

## Rules

- **Never edit an ingested source to "fix" an erratum.** The ingestion tree is a faithful capture;
  editing it destroys the only record of what the document actually said and silently rewrites the
  evidence for every finding that cites it.
- **Verbatim, with a locator.** Quote the source exactly and cite `file:line` in the ingestion
  tree, so the claim can be re-checked after the register moves.
- **Name the evidence tier** that establishes the correction — empirical/hardware-verified,
  `pnut-ts` legality, another Parallax document, or the document contradicting itself. A
  self-contradiction is the strongest report you can send, because it needs no external authority.
- **Distinguish OUR extraction defect from THEIR document defect.** If our derived extract says
  something the source does not, that is a correction-register item, not an erratum. Check the
  original capture before filing — E-006 was filed only after confirming the contradiction is
  verbatim in the 2020-edition text and not introduced by our summarisation.
- **`Reached our KB?` is mandatory.** It is what makes this a divergence map rather than a
  complaint list.

## Status vocabulary

`OPEN` — confirmed, not yet reported · `DRAFTED` — report text ready to send ·
`REPORTED <date>` — sent to Parallax · `ACKNOWLEDGED` — Parallax has responded ·
`FIXED <edition>` — corrected in a later edition; triggers a re-ingestion check ·
`WONTFIX` — Parallax has declined, and we carry the divergence permanently.

---

## Part A — confirmed errata

| # | Document @ edition | What it says (verbatim) | Why it is wrong | Evidence tier | Reached our KB? | Status |
|---|---|---|---|---|---|---|
| **E-001** | **P2 Hardware Manual** 2022-11-01, *Cog Attention* | `COGATN   #00001100` with the comment *"Get attention of cogs 2 and 3"* | Cogs 2 and 3 mean bits 2 and 3 = `%00001100` = 12. As printed, `#00001100` is **decimal 1,100** and does not assemble — *Constant must be from 0 to 511 (m130)*. **A `%` is missing.** | `pnut-ts` v1.55.3 rejects it (legality); confirmed verbatim in `word/document.xml`, so not an extraction artifact | **No** — never carried | `OPEN` |
| **E-002** | **P2 Hardware Manual** 2022-11-01, *SCOPE Data Pipe* (4 occurrences) | `ROLBYTE y,x` | `ROLBYTE` has exactly two legal forms — `ROLBYTE D,{#}S,#N` and the `ALTGB`-alias `ROLBYTE D`. The two-operand form errors *Expected ","*. Per the block's own comments (*"rotate pinN byte into y"*, reading the `RDPIN` lower byte) the intended form is **`ROLBYTE y,x,#0`**. | `pnut-ts` v1.55.3 rejects it; P2 Instructions v35 rows 94/95; confirmed in `word/document.xml` | **No** — never carried | `OPEN` |
| **E-003** | **P2 Hardware Manual** 2022-11-01, Table 10 (`%MMMMMMMMMM` note) | *"The VCO frequency should be kept within 100 MHz to **350 MHz**."* | **The manual contradicts itself twelve paragraphs later**: its own PLL prose (`p2-hardware-manual-text.txt:603`) reads *"designed to run between 100 MHz and **200 MHz** and should be kept within that range"* — verbatim identical to the Datasheet (`:850`) and the Silicon Doc (`:6233`). 350 MHz is real but it is the **VCO/1 overclock ceiling**, not the recommended range; the Silicon Doc says so in the very next row. The note substitutes the ceiling into the recommendation sentence. | **Self-contradiction** — needs no external authority. Corroborated by two other Parallax documents. | **No** — the KB follows the 100–200 MHz majority | `OPEN` |
| **E-004** | **#64013 P2 RTC Add-on Board Guide** v1.0 | *"…set the P2 Smartpin … **input mode** to 150 k-ohm pull-up"* (`P2-RTC-Add-on-text.txt:74-77`) | Wrong twice. (1) **The P2 has no pull-up resistors** — `P_HIGH_150K` selects a 150 kΩ *drive strength*; this is the exact mislabel F-321 exists to kill, appearing in a Parallax document. (2) **Input mode means `DIR` low**, and a drive selection does nothing while the pin is an input — so the prescribed configuration cannot work even on its own terms. | Empirical: **EF-063/EF-064** (`P2-EMPIRICAL-FINDINGS.md:827,840`) establish drive-with-DIR-high on silicon. Spin2 v55 `:1504` words it *"Drive high 150kΩ"*. | **Yes, open** — `hardware/addon-rtc.yaml` `pin_mode_tip` repeats it; deliberately **not** rewritten under D3/R9 pending this report. Owed to «#307». | `OPEN` |
| **E-005** | **#64000 P2 Eval Board Rev C Guide** §18 | SPI/SD pin directions for P58/P59 | The guide's §18 misstates the directions. Settled conclusively the other way: **P58 = MISO** (card DO, P2 input), **P59 = MOSI** (card DI, P2 output). | ROM booter listing `rom_booter_v33_01j.lst:135-138` declares `spi_di = 59` / `spi_do = 58`; the Silicon Doc boot table agrees and independently confirms P61=CLK, P60=CSn | **No** — the KB was already correct and stands unchanged. **Never cite §18** for these directions. | `OPEN` |
| **E-006** | **#64006 P2 Eval Add-on Boards Guide** 2020 edition | *"Each **active-high** push-button has a 470 Ω series resistor to allow the I/O pin to be **driven low** while the button is asserted."* (`p2-eval-add-on-boards-2020-edition-ocr-text.txt:45`) | **Active-high and driven-low-when-asserted cannot both be true of the same switch.** One sentence, both claims. | **Self-contradiction.** ⚠️ Verified as Parallax's, not ours: the contradiction is verbatim in the original capture, not introduced by our summarisation. | **Diverges** — `hardware/addon-control-board.yaml` says the pin *reads high* while pressed, resolving it the opposite way to the guide's second half. **See D-001 below — which reading is right is not yet settled.** | `OPEN` |

## Part B — framing differences, not errors

Two documents can both be right and still mislead a reader who takes one as "the range". These are
recorded so the KB **labels the distinction** rather than silently picking a side.

| # | Documents | The difference | What the KB must do | Status |
|---|---|---|---|---|
| **E-007** | **P2 Hardware Manual** *Specifications* vs **P2 Datasheet** *AC Characteristics* (p.48) | Manual: *"10–20 MHz crystal (PLL enabled) or 0 to 180 MHz (nominal) clock oscillator"*. Datasheet: Crystal (XI–XO) **1 min / 50 max MHz**; Direct drive **DC / 200 MHz**; PLL **3.33 / 320 MHz**. These are **recommended-use vs absolute-limit** statements, not a contradiction. | State which framing it is quoting, every time. Both sources agree on **180 MHz @ 105 °C nominal system clock**, so only the *input* limits need the label. | `OPEN` |

## Part C — open questions the errata raise

A defect in a source sometimes reveals that **nobody knows** the answer, ours included.

| # | Question | Why it is open | What would settle it |
|---|---|---|---|
| **D-001** | On the **#64006A Control** board, does a pressed button make the P2 pin read **high** or **low**? | E-006 shows the guide asserting both in one sentence. Our KB resolved it as *reads high*; the guide's mechanical description (470 Ω series resistor, *driven low while asserted*) implies *reads low*. **This determines whether generated code tests for high or low**, so it is actionable, not cosmetic. | A **bench test** on a #64006A — the board is a jumper-only rig, so this is runnable rather than catalogue-only. Or the board schematic from Parallax. |

---

## How an erratum gets here

`ingest-source` pass 6 (cross-source conflict audit) is the normal entry point: a conflict that
resolves to *"the source is wrong"* rather than *"our KB is wrong"* or *"nobody documents this"*
files here rather than to the corrections register or the gap ledger. A defect found later — during
a manual audit, a semantic read of an example, or a repopulation pass — files here too.

**The test for which register:** *if Parallax fixed their document tomorrow, would this entry
disappear?* Yes → it is an erratum. No → it is our correction, or a gap.
