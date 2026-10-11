# Close-out release — change-set audit (release-yamls §1.5), 2026-10-11

**Range:** `v1.23.3..HEAD` at `452322f6` — 180 commits; `deliverables/ai/P2/` 1,006 files changed
(+9,275 / −12,798 lines): 993 modified, 7 added, 6 deleted.
**Version:** v1.24.0, minor (Stephen, 2026-10-11).
**Verdict:** every confirmed finding is fixed, and the fixes were audited by an agent that made none
of them; Stephen decided the five review items (below) and they are applied. The release gate
(`validate-dod-release.py`, 28 checks) passes on the fixed tree.

## Method

Six fresh read-only auditors, split by file group, asked of every hunk: **wanted** (traces to a
finding, a decision or a report), **warranted and correct** (matches an ingested source at the line,
or an EF/CP record), **removals** (each deletion has a recorded reason; no `related:` lost), and
**complete** (the class search caught the siblings). A shared structural-diff tool
(`yamldiff.py`, scratch) parsed old and new YAML for every file, so mechanical classes (e.g. 356
`enhancement_source:` deletions) were proved by parse, not read by eye. Each returned finding was
hand-checked by the arbiter at the cited lines before acting.

| Group | Files | Hunks / differences | Confirmed | Suspect |
|---|---|---|---|---|
| A — PASM2 instructions a–i | 117 | ~300 (classes: enhancement_source deleted ~110; PASM2 Manual page cites ~107, checked against the PDF; ~45 content hunks read) | 0 | 4 |
| B — PASM2 j–z + concepts/groups/idioms/patterns | 285 | ~800 (page cites ~255, all checked; ~45 content hunks) | 4 | 5 |
| C — Spin2 + fundamentals | 310 | 4,892 structural differences | 8 | 8 |
| D — Community (OBEX 131, Quick Bytes 42) | 173 | 1,878 structural differences | 0 | 4 |
| E — architecture, hardware, app notes, guides, tools, non-YAML | 118 + 6 | 2,900 structural differences | 3 | 10 |
| F — standing checks over the whole delta | — | 6 checks | 2 | 5 |

## Standing checks (F)

- **Ingested documents untouched:** 8 modified files under `engineering/ingestion/` are all
  registers/ledgers (README dashboard, AUTHORITATIVE-SOURCES, DOCUMENT-LINEAGE, KNOWLEDGE-GAPS,
  SOURCE-ERRATA, the EF ledger, VERIFICATION-OPPORTUNITIES, a campaign README); every deleted line is
  a status flip or re-anchoring. 3 renames are identical-content moves of superseded HUB75 captures
  into `archived/`. 79 added files are new source captures (AK5704, PCF8523, HUB75 schematic +
  designer statement, Spin2 v55 operator reference), the compile-proof register and its proofs, and
  campaign tests.
- **Compile gate:** `--since v1.23.3` PASS, 3,166 blocks. The whole compile manifest is new in the
  range (630 files, additions only): no reclassification, no deleted entry; the 30 `never` entries
  are asserted to fail.
- **Cross-references:** no `related:` entry removed in the range.
- **Deleted files:** `.git-hooks/` (pointed at an obsolete path), `P2/CHANGELOG.md`,
  `PASM2-ENCODING-REFERENCE.md`, `pasm2/add-missing-oneliners.py` (no docs or scripts in the
  deliverables tree), `spin2/operators/op_addlteqgt.yaml` (an invented token, F-547).

## Findings and fixes

Confirmed findings, all fixed in this pass (100 YAML files, +2 docs):

1. **"Silicon Doc" nickname, "verbatim" markers, "line NNN", "ingested" in served text** — ~105
   lines in 51 files at first count, more found by the widened sweep (PASM2, Spin2, architecture,
   hardware, app notes, guides). Served text now states the fact; the citation, under the official
   title *Parallax Propeller 2 Documentation v35 (Rev B/C Silicon)* and its section, sits in a
   stripped source field. Three keys renamed: `datasheet_note_verbatim` → `datasheet_note`,
   `verbatim` → `parallax_text`, `measured` → `observed_failures`.
2. **Provenance and process remarks in served text** — the seven hub-operand `immediate_address_note`
   blocks ("Authority: PNut-TS v1.55 …"); E1 strings in rdlong/wrlong/wmlong/setq ("Source: …; step
   measured (ALTD tested)"); augs `scope_note`; orgh "-- compiler-verified"; the Spin2 operators page
   compile date and tool version; op_POW process note; "measured/proven/tested" wording in getxacc,
   rdfast, cordic, pin-selection; p2an007's date and repo path; cordic's EF-053 in served text.
3. **Wrong facts** — `word.yaml` said WORD data is automatically word-aligned (DAT data is packed in
   order; ALIGNW aligns), Spin2 v55 DAT Blocks.
4. **Unsourced claims** — muxq comparatives ("faster", "more efficient", "critical for"); p2an004's
   TSL235R calibration figures and "check it before relying on it" (the datasheet is held only as
   uningested app-note fodder, so it is not citable); `p2-hardware-feature-comparison.yaml` cost
   tiers, six `educational_rating` values and two `corrections_applied_2026_08_25` change-history
   blocks; `created:`/`updated:` stamps in two architecture files; forum pointers in p2an001,
   multi_resource_management and smart-pin %11011.
5. **Claims true but unrecorded** — proved and recorded as compile proofs:
   CP-010 (OBEX 2842 `jm_fullduplexserial.spin2` does not compile: a local named `field`, m241),
   CP-011 (the COMP/SWAP methods need `{Spin2_v45}`; the compiler refuses the v44 the v55 table
   names), CP-012 (ORGH limit errors m361/m372 and the PASM-only debug-mirror failure).
6. **Citations that did not say what they cite** — p2an005 TASKHLT `$1CC` (from the Spin2
   Interpreter v55 register layout, not the documentation); the HUB EXECUTION section cited for the
   (cogs+11) FIFO depth (THE COG -to- HUB RAM INTERFACE) and the REP hidden jump (INSTRUCTION
   REPEATING); locks.yaml lock 15 now cites v55 DEBUG ("LOCK[15] is allocated by the debugger").
7. **Removals without a reason** — `sqrt.yaml` restored its `SQRT(2)` example, "Maximum result is
   65535" and the 0-65535 range (consistent with `op_SQRT.yaml`).
8. **Incomplete class sweeps** — erratum labels and the hub link added to the E1 pages (setq,
   rdlong, wrlong, wmlong), the ALTx pages (link only), Spin2 GETMS/GETSEC (E3) and WRPIN (E6, a new
   `silicon_errata` block from the hub page, EF-071); inline-PASM pages no longer teach the `:label`
   form decision D6 removed; `addon-hd-audio.yaml` gained the base-pin options and P56-P63 caution
   its 15 siblings carry (the HD Audio guide: any single accessory socket, offsets 0-7);
   `addon-wx-adapter.yaml` states that base_pin 56 is the documented wireless-programming placement
   and what it shares.
9. **Dangling link** — `deliverables/ai/README.md` pointed at the deleted `P2/CHANGELOG.md`; now
   the repository `CHANGELOG.md`.
10. **Fix-introduced defects caught by the gates and fixed** — two `sources:` lists at column 0
    (stripping the key would have attached the item to `notes`); three duplicate `source:` keys;
    CP-011's KB-home paths.

### Recorded reasons for removals the auditors could not trace

- `pasm2/concepts/register_indirection.yaml` `computed_jump`, `switch_case`, and
  `branch_addressing.yaml` `table_dispatch`: the patterns used `ALTS … JMP #0-0`, but `JMP #A`
  takes a 20-bit A field, not S, so ALTS does not redirect it. The examples were wrong.
- `register_indirection.yaml` `limitations` "Cannot modify ALTx instructions themselves": wrong —
  an ALTx alters the next instruction regardless of its kind, another ALTx included (PASM2 Manual,
  ALTS; study row S-217).
- `hardware/addon-wx-wifi.yaml` serial-mode, command-mode and firmware facts: they came from the
  32420 Wi-Fi Module API Guide, held only in a NO-COMMIT folder and not ingested, so not citable
  (Stephen's review item c).
- `hubexec.yaml` Chip Gracey's forum clarification: forum material is a lead, not a citation; the
  claim now rests on the HUB EXECUTION forbidden list.
- `extraction_status` on 131 OBEX objects: study row S-327 (provenance keys that ship but are not
  citations).

## Verified, no change

- OBEX/Quick Bytes: the `metadata:` → `scrape_tracking:` rename is exact (no `object_metadata`
  touched); `last_scraped` moves have identical values; Quick Bytes URLs all match the re-rooted
  shape (not fetched); the `code_author` placeholder emptied.
- HUB75 schematic and designer-statement facts; AK5704 and PCF8523 chip blocks against their
  datasheets; P56-P63 caution present on every page whose base pins reach P56, and on none that do
  not; `silicon_errata.yaml` E1-E7 against EF records and the KNOWN SILICON BUGS text; QSQRT/SQRT
  truncation (EF-104).
- PASM2 Manual page citations (~360) against the PDF page footers.

## Stephen's review — decisions (2026-10-11)

Stephen set this release as the point where refinement stops and release and testing begin:
whatever already ships in v1.23.3 and is left alone here is no worse than today.

a. **Labelled unsourced guidance — removed.** `cogspin.yaml` drops the 32 and 64-128 longs
   figures and states that no Parallax document gives a size; the measurement procedure stays and
   points at P2AN006. The same figures were removed from `spin2_cog_management.yaml`
   (`sizing_guidance`), from the P2AN006 companion YAML and from the P2AN006 MANUAL-DESCRIPTOR
   (the published note never carried them). `p2-hardware-feature-comparison.yaml` drops every block
   authored here with no source, not only the two named: `educational_progression`,
   `application_domains`, `selection_criteria` (its own source said "authored in this knowledge
   base and have no upstream source"), the `edge_module_carriers` perfect/optimal/good ratings,
   `recommended_combinations`, `summary_recommendations`, and three unsourced notes ("Add-on boards
   require P2 Eval Board for full functionality", "Breakout boards ... require external
   programming setup", "Educational progression ..."). Left in place: the per-board
   `educational_concepts` and `complexity_level` labels (shipping in v1.23.3, unmarked, out of
   this release's scope by Stephen's stop line).
b. **HUB75 residue — left as is**, except "unpopulated" on the spare holes: it was added in this
   release and contradicts the schematic ("so can populate"), so it was removed. The other new
   statements ("own 5 V supply", the chipset lines) rest at least partly on the schematic.
c. **WX Wi-Fi API facts — stay removed.** The guide is not ingested; v1.24.0 tells the agent less
   about the WX module than v1.23.3 did, and nothing wrong.
d. **Eval header pairing — left as is.** Shipping unchanged in v1.23.3 in all five files.
e. **Bench-confidence wording — moved out of served text.** Principle (Stephen): the agent is told
   facts and believes them; keeping them correct is our job, and trust or verification status is
   not fed forward. Each served line now states the fact; its EF/CP id and evidence scope sit in a
   stripped source field; dates removed. A filter-aware search found about 60 served lines, not the
   37 first counted (the first count missed "Measured:" labels and evidence-scoping qualifiers).

**Version:** minor, v1.24.0 (Stephen, 2026-10-11): the delivery filter is a new index capability
(index format 3.6.0). If test-plan step 3 shows the old MCP cannot load it, that is a defect fixed
before the tag, not a reason for a major bump.

## Not checked

- Quick Bytes `has_code`/`download_count` values and the 12 renamed slugs against the live pages
  (no fetch).
- Interpreter-listing claims cited from the close-out study's specs were not re-read line by line.
- Image-only facts (board silkscreen, schematic images).
