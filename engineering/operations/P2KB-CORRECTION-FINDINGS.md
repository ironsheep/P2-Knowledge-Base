# P2KB Correction Findings — Consolidated Register

**Purpose:** the register of everything we find that is **wrong or needs correction** — primarily in the P2 Knowledge Base YAML (`deliverables/ai/P2/`), but also any other source/content correctness issue worth tracking. This is the hand-off document for the agent that corrects the P2KB (via `yaml-knowledge-base-maintenance`).

**This file carries OPEN work only.** Closed findings are archived, not kept here. Ask "what is
outstanding?" of this file alone — never re-derive completion state from an archive.

**How to use it:**
- When any work (manual production, audits, example compilation, ingestion, bench) surfaces something incorrect, **add it here** — do not leave it only in a per-manual note.
- Each finding gets an ID, a status, the exact location, what is wrong, the evidence, and the proposed correction.
- **Annotate as you fix, in the same pass** — flip the status, add an applied-note and source trace, and log newly-surfaced defects as new findings. A register whose statuses lag the YAML lies and invites re-chasing.
- **One finding lives in exactly one place.** When a finding is revised, **rewrite its entry in place**; never append a correction below the entry it corrects. The prior text is in git and in the archives.
- Consultation protocol (status-before-content, duplicate IDs are a STOP): the project's
  `REGISTER-CONSULTATION` protocol (agent-side; not shipped with this repo).

**Status legend:** `CONFIRMED` (verified against an authority; ready to fix) · `NEEDS-VERIFICATION` (suspected; must be checked before acting) · `PARTIAL` (some of it applied; the rest still owed) · `PENDING-VALIDATION` (the fix is fully applied; only its validation — a render, a release, a re-test — is owed. Added 2026-08-21: the rule below already described this state and there was no token for it, so nine findings sat as `CONFIRMED` with "render owed" prose and tripped the hygiene gate on every run) · `DONE` (corrected + verified) · `WONTFIX` (investigated, not a defect) · `RESOLVED-INVALID` (the reported defect does not exist) · `TRACKED → ingestion` (real, but the resolution lives in the ingestion head) · **`RESOLVED`** (the defect is gone AND its validation has landed — the render/release/re-test was RUN and the artifact READ; a fix applied but unvalidated is `PENDING-VALIDATION`, never this. **Added to this legend 2026-08-25 («#302»): it was already the file's MOST-USED token — 31 of 82 entries — and the legend had never defined it, so a third of the register could not be classified by the very vocabulary this line exists to declare**) · `PARTIALLY CONFIRMED` (a ONE-OFF variant used only by F-202, where part of the claim is grounded in a source and part awaits silicon; it classifies as **`CONFIRMED` — open** — do not spread it).

⚠️ **`RESOLVED` entries are CLOSED and are awaiting the next archive sweep, not awaiting work.** Since 2026-10-05 the hygiene gate treats a live `RESOLVED` exactly like a live `DONE` — closed-but-live, a violation — so this file can only read CLEAN while it carries open work alone. Before that the gate let `RESOLVED` through, and closed findings piled up behind a CLEAN verdict: 119 of 179 live entries, with "what is outstanding?" overstated by two-thirds, until the «#386» reconciliation verified every entry against the tree and the release tags and swept the 130 closed ones (`correction-sweeps/2026-10-05-register-reconciliation-…`). **Close a finding by sweeping it, in the same pass that closes it.**

**A fix applied but not yet validated is NOT done** — it stays here until its validation lands (the `[~]` rule from `punch-list-maintenance`). That covers a YAML edit awaiting its EF entry, and a manual fix awaiting its re-test.

**Authority order for P2 facts:** empirical / hardware-verified results in `engineering/ingestion/external-sources/hardware-verification/` (strongest — they have overturned every other tier) → the `pnut-ts` compiler, for legality only → Parallax documentary sources under `engineering/ingestion/sources/` → the published P2KB YAML. Community/forum material is an upstream lead, never a citable authority.

**No inference or derivation.** Every correction must trace to an authoritative source. Aligning a file to an authority it contradicts is fine; **inventing a value or claim that no source states — by computation, reasoning, or "it must logically be" — is not.** If a change can only be justified by inference, log it as a finding that needs a source. Match the source's wording, not an interpretive paraphrase.

**Next finding ID: `F-643`** · gap IDs are **not allocated here** — `engineering/ingestion/KNOWLEDGE-GAPS.md` owns the `G-` allocator and declares its own counter. (This line previously carried `Next gap ID: G-008`, stale by fourteen against that register's actual G-022; two registers claiming one allocator is the collision `audit-register-hygiene.py` exists to catch. Retired 2026-08-26 — see F-352 for the earlier, smaller instance of the same drift.)

**Archives** — search them before re-filing; a finding that reappears is usually a regression:
- F-001…F-124 → `correction-sweeps/2026-06-13-P2KB-CORRECTION-FINDINGS-archive.md`
- F-125…F-266 (closed) → `correction-sweeps/2026-08-15-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-08-19 (18 findings: F-227, F-228, F-254, F-255, F-257, F-258, F-259, F-260, F-261, F-262, F-263, F-264, F-265, F-266, F-267, F-269, F-270, F-273) → `correction-sweeps/2026-08-19-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-09-10 (1 finding: F-415, `RESOLVED-INVALID`) → `correction-sweeps/2026-09-10-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-01 (24 findings: F-449, F-450, F-451, F-452, F-462, F-463, F-464, F-465, F-466, F-467, F-468, F-469, F-470, F-471, F-472, F-473, F-474, F-475, F-476, F-477, F-478, F-480, F-481, F-482) → `correction-sweeps/2026-10-01-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-03 (45 findings: F-440, F-445, F-446, F-447, F-448, F-483…F-505, F-506…F-520, F-522) → `correction-sweeps/2026-10-03-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 (4 findings: F-400, F-523, F-526, F-540) → `correction-sweeps/2026-10-04-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the manual releases (2 findings: F-521, F-524) → `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Debug Window v1.1.4 release (1 finding: F-531) → `correction-sweeps/2026-10-04-debug-window-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-04 after the Streamer Guide v1.1.3 release (2 findings: F-539, F-479) → `correction-sweeps/2026-10-04-streamer-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the XBYTE Guide v1.1.1 release (2 findings: F-537, F-538) → `correction-sweeps/2026-10-05-xbyte-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the I/O & Smart Pins v1.0.11 release (4 findings: F-533, F-534, F-535, F-536) → `correction-sweeps/2026-10-05-iosp-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the Assembly Reference v3.1.11 release (4 findings: F-527 `RESOLVED-INVALID`, F-528, F-530, F-541) → `correction-sweeps/2026-10-05-assembly-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 after the deSilva v3.0.9 release (3 findings: F-529, F-532, F-276) → `correction-sweeps/2026-10-05-desilva-release-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-05 by the register reconciliation «#386» (130 findings verified closed against the tree and the release tags; 63 emptied section headings moved with them) → `correction-sweeps/2026-10-05-register-reconciliation-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-10 by the close-out sprint «#423» (5 findings with nothing left to validate or ship: F-218, F-336, F-364, F-405, F-441) → `correction-sweeps/2026-10-10-close-out-sprint-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-11 by the close-out release MCP validation «#398» (34 findings: F-381, F-383, F-386, F-387, F-389, F-392, F-393, F-398, F-421, F-436, F-439, F-454, F-525, F-542, F-543, F-544, F-546, F-547, F-548, F-549, F-550, F-551, F-552, F-553, F-554, F-555, F-556, F-557, F-558, F-559, F-560, F-563, F-568, F-570) → `correction-sweeps/2026-10-11-mcp-validation-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-11 at the v1.24.1 release «#398» (1 finding: F-572) → `correction-sweeps/2026-10-11-v1.24.1-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-12 at the v1.24.3 release «#425» (1 finding: F-573) → `correction-sweeps/2026-10-12-v1.24.3-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-12 at the v1.24.5 release (1 finding: F-574) → `correction-sweeps/2026-10-12-v1.24.5-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-05 at the v1.25.0 release (49 findings: F-576 … F-615, F-617 … F-624, F-629; F-588 and F-589 withdrawn) → `correction-sweeps/2026-11-05-v1.25.0-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-07 at the Assembly Reference v3.1.12 release (F-625, F-626, F-631, F-634, F-635, F-639, F-268) → `correction-sweeps/2026-11-07-assembly-v3.1.12-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-07, KB findings served (F-637, F-636, F-569, F-567, F-564, F-545, F-377, F-375, F-372, F-361, F-359, F-352, F-347, F-337, F-320) → `correction-sweeps/2026-11-07-kb-closure-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-07 at the I/O & Smart Pins v1.0.12 release (F-356, F-202) → `correction-sweeps/2026-11-07-iosp-v1.0.12-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the XBYTE Guide v1.1.2 release (F-627, F-628) → `correction-sweeps/2026-11-06-xbyte-v1.1.2-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the P2AN003 v1.0.3 release (F-561) → `correction-sweeps/2026-11-06-p2an003-v1.0.3-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the P2AN007 v1.0.4 release (F-565) → `correction-sweeps/2026-11-06-p2an007-v1.0.4-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the P2AN004 v1.0.4 release (F-638) → `correction-sweeps/2026-11-06-p2an004-v1.0.4-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the P2AN007 v1.0.3 release (F-630) → `correction-sweeps/2026-11-06-p2an007-v1.0.3-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-11-06 at the v1.25.1 release (F-632, F-633) → `correction-sweeps/2026-11-06-v1.25.1-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-15 by «#434» (1 ID never used: F-616, `RESOLVED-INVALID`) → `correction-sweeps/2026-10-15-unused-id-P2KB-CORRECTION-FINDINGS-archive.md`
- closed 2026-10-12 at the P2AN006 v1.0.2 / v1.24.6 release (1 finding: F-575) → `correction-sweeps/2026-10-12-p2an006-v1.0.2-P2KB-CORRECTION-FINDINGS-archive.md`

> **Swept 2026-08-19** per `punch-list-maintenance`, as **rename-then-trim** (the archive is a
> git-tracked rename of the original; both files are subtractions from a preserved copy — see the
> skill's project overlay for why building the output loses content). 18 findings archived, 3,559 →
> 2,478 lines. **Classified by STATUS TOKEN only.** Sixteen findings whose headline reads "source
> fixed"/"tool fixed" **stayed open**, because their status is still `CONFIRMED` and most say
> "render owed" — this file's own rule is that a fix applied but not yet validated is NOT done. A
> first pass that trusted the prose would have archived all sixteen. Verified with
> `audit-register-hygiene.py --sweep-check`, which reads the pre-sweep revision out of git.
>
> **Swept 2026-08-15** per `punch-list-maintenance`: 129 closed findings archived, 3,161 lines → this
> file. The previous sweep was deferred on 2026-06-20 pending G-004 and G-005; G-005 closed
> 2026-07-04, and G-004's remainder was found to be out of KB scope entirely (see its entry), so the
> deferral's condition is discharged.

---

## Found by the contract-gaps sprint (2026-11-09) — F-643

### F-643 — what `COGINIT()` returns when no cog is free: the Spin2 document and the interpreter listing disagree — `NEEDS-VERIFICATION` (found 2026-11-09, «#462»)
> **KB decision:** held (bench): a run with all eight cogs busy, added to the contract-gaps bench visit
`spin2-v55-text.txt:517` says the method returns -1 when no cog is free. The Spin2 interpreter v55 (lines 1104-1105) runs `coginit x,y wc`, then `_ret_ bitc x,#31`; the Silicon Doc (`silicon-doc-text.txt:386`) says a failed COGINIT writes $F into D with C set, and BITC writes C into bit 31. Read together, the listing's path returns $8000_000F. The served text and the `IF cog == -1` examples stay as the Spin2 document has them until the run decides. COGSPIN's return needs the same check.

## Found by the RFVAR/RFVARS change «#440» (2026-11-05) — F-640 … F-642 (F-625 … F-639 archived)

### F-642 — Assembly Chapter 5 keeps "interrupt-free zone" where the REP entry says "shielded block" — `CONFIRMED` (found 2026-11-07, the Assembly v3.1.12 verification)
> **KB decision:** not KB: Assembly master, fixed at its next release
Accurate, and it fails no gate; the two passages only differ in wording. `chapter-05-hardware.md:209` and `:219` (p101) say "interrupt-free zone", and F-635's pass changed the same sentence in `instructions-r.md` to "shielded block" (p296). Fix: use the Silicon Doc's "shielded" at both.

### F-641 — two layout blemishes seen reading released pages — `CONFIRMED` (found 2026-11-06, the Debug Window and deSilva verification)
> **KB decision:** not KB: document masters, fixed at each document's next release
Neither misstates anything, and neither fails a gate. Debug Window v1.1.5 p109: the first line of the note at `ch10-spectro.md:222` ends 19.3pt past the right margin at `RGB8/16/24,` (45.29pt overfull in the log), inside the margin gate's 20pt tolerance and the same line as in v1.1.4. Fix: reword so the list breaks earlier. deSilva v3.0.10 p43: the code span `long @` splits across a line, printing `LONG` at the end of one line and an indented ` @` at the start of the next. Fix: reword so the span does not fall at a line end, or write it as `long @label`.

### F-640 — `spin2-pasm2-integration.yaml` `mixed_execution_modes` jumps with `#\@sym` in a Spin2 object — `CONFIRMED` (found 2026-11-06, the v1.25.5 live read)
> **KB decision:** in batch v1.26.0
Lines 359, 362, 363, with `PUB start()` in the same block. A `pnut-ts` probe encodes `jmp #\@hs` as absolute with the object offset (`$10`, the symbol at `$1898` in the image). F-639's sweep searched `##@`, `#@` and `@@` and missed this form. A search of the KB and every document master finds it nowhere else. No document is affected. The sweep by operand also reads `manuals/p2-errata/code-validation/test-briefs/BRIEF-SO109.md:383-395,472`, whose `##mbox` and `##tgt_hub` are F-639's class: a git-ignored test brief, not a printed document.

---




## Found during the 2026-10 manual releases, the register reconciliation and the pre-release audit (2026-10-04/07) — F-546 … F-562 (+ F-563, found 2026-10-09 by the VO-J-035 rework; + F-564, found 2026-10-09 by «#414»; + F-565, found 2026-10-09 by «#415»; + F-566, found 2026-10-10 by «#422»; + F-567, found 2026-10-10 by «#422»/«#423»; + F-568, F-569, found 2026-10-10 by «#422»; + F-570, reported 2026-10-10 by Stephen; + F-571, F-572, F-573, found 2026-10-11 by «#398» and the MCP agent's 1.5.1 review; + F-574, reported 2026-10-12 by Stephen; + F-575, found 2026-10-12 by the debug-techniques study; + F-576 … F-583, found 2026-10-13 by «#430» from the debug-techniques claim ledger; + F-584, found 2026-10-13 by «#430»'s independent check; + F-585 … F-600, found 2026-10-13 by «#430» batch 2 (Spin2 / debug pages, phase W part 1); + F-601 … F-613, found 2026-10-13 by «#430» batch 2 (hardware / smart-pin / streamer pages and the arbiter's part-1 follow-ups, phase W part 2); + F-614 … F-615, found 2026-10-13 by «#430»'s Phase S sourcing audit (pre-existing claims no golden source states); + F-617 … F-624, found 2026-10-15 by the debug toolbox's «#434» B0 (served defects and their whole class). F-616 was never filed: the arbiter read the `Next finding ID: F-616` line as the last ID used and allocated from F-617.) (F-564, F-567, F-569 archived)
Fixed 2026-11-09 (task «#464»). The `mixed_execution_modes` block now starts the cog with `COGINIT(COGEXEC_NEW, @fastCode, @slowCode)`, so the run-time hub address of `slowCode` arrives in the new cog's PTRA; the cog code ends with `JMP ptra`, the hub code calls `complexMath` with the relative `CALL #complexMath`, and jumps back to cog address 0 with `JMP #\fastLoop`. A `pnut-ts` 1.55.10 listing decodes the three control-transfer words as `JMP ptra` = `$FD63F02C` (D = `$1F8`, PTRA), `CALL #complexMath` = `$FDB00004` (relative, +4 from the next long = `complexMath`) and `JMP #\fastLoop` = `$FD800000` (absolute, cog address 0). The block compiles in a Spin2 object under `audit-kb-code-compiles.py --files`. Sweep by operand (2026-11-09): the backslash-at form `#\@` appears in the KB only in `branch_addressing.yaml` (4 lines, a PASM-only table from the Silicon Doc, correct) and in the F-640 block; the backslash form `#\sym` has 35 lines in 13 YAML files (after the rewrite), none a hub symbol in a Spin2 object; `##@` 21 lines, `#@` 11, `@@` all in Spin2 methods, `LONG/WORD @` all stated as object offsets; every hub-symbol `##` or `#` fragment sits in a file that carries the PASM-only `hub_symbols` note or says PASM-only in place. Masters: no `#\@` hit in any of the 14 `opus-master` folders; three master examples use `#\hubsym` or `#hubsym` with a hub symbol (deSilva `COMPLETE-OPUS-MASTER.md` 3360, 3438, 3518, 4393; Assembly manual `instructions-r.md` 601) and each document states that its hub-symbol fragments are PASM-only. No document is affected. `BRIEF-SO109.md` 383-395 and 472: `mbox`, `isr_hub` and `tgt_hub` are defined as constants (the brief says so at 477-478), so `##mbox` is a literal address, not a DAT label.

### F-571 — `p2kb_obex_get` shows a zero quality score and an empty created date for every OBEX object — `PARTIAL` (found 2026-10-11 by the close-out release MCP test, step 5, «#398»; the date moved KB-side 2026-10-11 for v1.24.1; the KB is a pure mirror from v1.24.4; the server half, including dead download links, is requested for p2kb-mcp 1.5.1)
> **KB decision:** not KB: the p2kb-mcp server half
**Updated 2026-10-12 (KB v1.24.4, "pure mirror"):**
- Every object is now the catalog's fields only. `version`, `file_size`, `author_username` and the
  other fields the server's struct reads are gone. The change request (§2, §3.2, §3.3) now asks the
  server to drop them too.
- All 130 objects carry a date: 2816's came back with the v1.24.2 mirror.
- **New for 1.5.1 (§3.6):** 5 objects (4442, 4571, 4581, 4616, 4617) have no download on OBEX, and
  their YAML now has no `download_direct`. A server that builds the URL from the id hands agents a
  link that answers `invalid!`. The request asks the server to take `download_url` from
  `urls.download_direct` and omit it when absent. Probe O3 now tests this (4581), replacing the
  2816 no-date probe.
- `scrape-obex-repos.py` is retired; `obex-catalog-mirror.py` writes the date.

**Applied 2026-10-11 (Stephen: "yes a now"):** the upload date moved from
`version_tracking.obex_upload_date` to `object_metadata.metadata.created_date` in all 129 objects that
had one then. Proved against HEAD: all 131 files (130 objects and the template) parse equal to before apart from that move (and 2842's
`known_issues` clearing). **Requested for p2kb-mcp 1.5.1** (Stephen, 2026-10-11):
`engineering/tools/p2kb-mcp/MCP-OBEX-SUMMARY-CHANGE-REQUEST.md` — remove `quality`, omit empty fields,
drop dead struct fields, add `full_metadata` (the whole filtered object, ending field-name coupling);
acceptance probes O1-O7 there. `OBEX-IMPLEMENTATION-SPEC.md` and `P2KB-MCP-SPECIFICATION.md` updated
to the same contract. **Date half validated live 2026-10-11** on p2kb-mcp 1.5.0 against v1.24.1:
`p2kb_obex_get 2842` → `metadata.created_date: "2022-01-04"`; 2816 → `""` (no date). `quality: 0`
remains until 1.5.1. **Release-day note:** the first refreshes after the push ran inside GitHub raw's
5-minute CDN window — a normal refresh reported 0 stale keys and kept pre-release bodies, and a flush
inside the window made every OBEX object fail verification (old bodies vs new index: "not found",
"verification failed"). A flush after the window cleared both. Probe a release only after ~5 minutes.
Probed on p2kb-mcp **1.5.0** against KB v1.24.0, after `p2kb_refresh include_obex` (0 stale entries).
`p2kb_obex_get 2842` returns a curated summary, not the object. **What the server reads** — the YAML
tags compiled into the v1.5.0 linux-amd64 binary: `object_metadata` → `title`, `author`,
`author_username`, `urls.*`, `technical_details.*`, `functionality.*`, and a block `metadata` →
`created_date`, `quality_score`, `discovery_date`, `last_verified`, `extraction_status`. It parses no
`compatibility` and no `version_tracking`. (`engineering/tools/p2kb-mcp/OBEX-IMPLEMENTATION-SPEC.md`
specifies a `full_metadata` field — the whole object — which the server does not return.)
- `metadata.quality: 0` — the KB removed `quality_score` («#422»; we do not rate OBEX objects), so the
  server shows Go's zero value, which reads as a rating of zero. **Server-side only:** no KB value can
  remove it short of inventing a score.
- `metadata.created_date: ""` — `object_metadata.metadata` was renamed `scrape_tracking` (filtered at
  delivery; F-545), so the server finds nothing. The real upload date is served as
  `version_tracking.obex_upload_date` (`'2022-01-04'` for 2842; 129 of the 130 objects carry one).
  **KB-side option:** move it to `object_metadata.metadata.created_date` (a fact about the object, not
  scraper bookkeeping) and have `scrape-obex-repos.py` write it there — the server then shows it with no
  change. Stephen's call, asked 2026-10-11.

**`known_issues` is withdrawn from this finding (Stephen, 2026-10-11):** "It's not up to us to be rating
OBEX content." The CP-010 compile verdict was removed from object 2842 and from the four pages that
repeated it (three JonnyMac convention pages, the Spin2 getting-started guide); the language fact it
rests on — `field` cannot name a method local — now lives on `language/spin2/operators/FIELD.yaml`, and
CP-010's KB home moved there. Doctrine overlay: *An OBEX entry carries what the catalog says, never our
verdict on it.*

**The KB body is correct:** `p2kb_get p2kbCommunity2842` serves the filtered object (no
`scrape_tracking`). v1.4.0 showed the same summary mapping (test record step 3,
`correction-sweeps/2026-10-11-close-out-release-mcp-test.md`, git-ignored).
**Owed:** the date per Stephen's call; in the MCP server, drop `quality` (or return the whole filtered
object as the OBEX spec says, which ends field-name coupling for good). Re-probe 2842 on the release
that carries each.

### F-566 — Parallax moved www.parallax.com to Shopify; every Quick Bytes article now lives on the OBEX docs site, so all 42 catalog entries cited a dead root — `PENDING-VALIDATION` (applied 2026-10-10, «#422»; closes when the next KB release serves it)
> **KB decision:** held (Stephen): whether to probe the other www.parallax.com links, left unprobed at his request to keep traffic to Parallax light
Found 2026-10-10 by «#422» checking S-390: `community/quick-bytes/simple-analog-input.yaml` cited
`https://www.parallax.com/simple-analog-input/`, which returned HTTP 404. Stephen's reading: the site moved, so
"quick bytes urls may have changed ... all should be rerooted the same way". **Applied:** all 42 entries in
`community/quick-bytes/` now cite `https://obex.parallax.com/docs/quick-bytes/propeller-2/<slug>/` in `url:`,
`modalities.article` and `modalities.source_code.get_from` (the arbiter fetched each: HTTP 200). 30 slugs were
unchanged; 12 moved and `slug:` is updated (the filenames keep the old slugs — they are KB keys):
`breakout-board-options-for-p2`, `dht11-dht22-cm2302-object`, `floating-point-math`, `i2c-device-bus-scanner`,
`i-o-test-utility-with-led-matrix`, `multiple-serial-port-16-object`, `p2-simple-video-driver-using-images-intro-to-using-video-2-of-3`,
`rotary-encoder`, `smart-pins-tsl235r`, `video-hardware-character-map`, `visual-studio`, `wireless-programming`.
The six hardware pages that linked a Quick Bytes article (`addon-goertzel-touch`, `addon-control-board`,
`addon-av-breakout` x3, `addon-led-matrix`) were re-rooted the same way. **Downloads:** the old
`download_mechanism: parallax-download-manager` is gone; each article page now lists its code as plain
`/qbi/downloads/<file>` links on `obex.parallax.com` with no login wording on the page, so the field reads
`direct-link`. `download_count` / `has_code` were corrected to what each page lists (flash reader 4→6, neopixel
1→3, rotary 3→4, 32-channel ADC 1→2, DHT 2→1, DS3231 2→1, LED-matrix test 3→1; multi-servo, floating-point and
serial-16 `has_code` false→true; wireless programming true→false, its page offers only a Google Drive
firmware link, already in `reference_links`). `addon-av-breakout`'s character-map `source_package` now names
the file the page lists. **`code_author` of `simple-analog-input.yaml`:** the new page's Document Author and
Source Code Author blocks read "John Doe" and "Jane Doe" — template placeholders, not authors — so `code_author`
stays `''` and `author: Ken Gracey` stands (the page carries no published date). The claim-sourcing gate
(`audit-yaml-claim-sourcing.py` `CATALOG_URL_RE`) now accepts the `obex.parallax.com/docs/quick-bytes/` root
beside `parallax.com/`; a non-Parallax host is still refused. **Owed:** other `www.parallax.com` links in the
hardware pages that are not Quick Bytes articles (`/usbdrivers`, `/product/p2-to-mikrobus-click-adapter`, the
bare home page) were not probed under the request to keep traffic to Parallax light; and the download links
themselves were read from the pages, not fetched, so `auth_gated: false` rests on the page showing no gate.

### F-562 — `hub75_adapter.yaml` names the OBEX driver and URL differently from OBEX 2850's own metadata — `NEEDS-VERIFICATION`
> **KB decision:** held (Stephen): the entry waits for him to open the live OBEX listing
Found 2026-10-07 by the independent check of F-556. `hardware/hub75_adapter.yaml:156,158` gives
"P2-HUB75 LED Matrix Driver" and `https://obex.parallax.com/obex/p2-hub75-led-matrix-driver/`;
`engineering/ingestion/external-inputs/source-code/obex-projects/2850-ISP_Hub75_Matrix_Driver/2850_metadata.yaml:51,57`
gives "ISP Hub75 Matrix Driver" and `.../isp-hub75-matrix-driver/`. Which is current is unverified
(no network probe here). **Fix:** confirm against the OBEX listing the user can open; use that.

> **Applied 2026-10-10 («#420»); the entry stays NEEDS-VERIFICATION until Stephen opens the live
> listing.** `hub75_adapter.yaml` `resources.obex` now reads "ISP Hub75 Matrix Driver" and
> `https://obex.parallax.com/obex/isp-hub75-matrix-driver/` — the form in `2850_metadata.yaml:51,57`
> (downloaded 2025-09-13) and in the KB's own OBEX object page (`community/obex/objects/2850.yaml:50,56`),
> which already agreed with each other; the old name was the GitHub repository's. **Not verifiable
> here:** whether the live OBEX listing still carries that title and path (no network). Stephen:
> open `https://obex.parallax.com/obex/isp-hub75-matrix-driver/` and say if it resolves.

## Impact survey — v1.25.0 (`release-yamls` §8, run 2026-11-05)

The v1.25.0 delta (80 YAMLs) was intersected against every live document's declared sources, then each
intersecting master was grepped for the statements the delta contradicts. Each row is a
**re-audit-against-HEAD** signal for that document's next pass.

| Document | What changed in the KB | Located in the manual |
|---|---|---|
| Assembly Reference | RFVAR/RFVARS format, FVAR/FVARS; DEBUG_DISABLE scope; REP and interrupts; TESTP in a smart-pin mode | F-625, F-626, **F-631** |
| Interpreters & Emulators (XBYTE) | RFVAR/RFVARS format, FVAR/FVARS | F-627, F-628 |
| P2AN007 | LOCKNEW's failure value is negative, not `-1` | `P2AN007.md:277`, `:424` — **F-630**; its companion already says it |
| DeSilva Tutorial | PASM2 descriptions, REP and interrupts, TESTP | no contradicted statement found by the grep; to the audit |
| I/O & Smart Pins | `%11101` IN and clocking, `%01110` as observer, smart-pin IN as a flag, Edge neighbour reach | no contradicted statement found by the grep; to the audit |
| Streamer Guide | capture with the smart pin off; XINIT count not range-checked | no contradicted statement found by the grep; to the audit |
| Getting Started | `hub`, boot pins, `spin2-getting-started` | no contradicted statement found by the grep; to the audit |
| Architect's Guide | `resource-ownership`, `locks`, `hub` | no contradicted statement found by the grep; to the audit |
| P2 Errata | `language/pasm2` is an authoring aid there | no contradicted statement found by the grep |
| P2AN006 | `cogspin` stack wording | no contradicted statement found by the grep; to the audit |

No declared source of the DEBUG Window Manual, Single-Step Debugger, PNut-Term-TS guide or P2AN001-P2AN005
reaches a changed fact (the P2AN004 companion's change is a `source:` field; P2AN001's `rdpin` change is a
description's table residue).

## Impact survey — v1.24.6 (`release-yamls` §8, run 2026-10-12)

v1.24.6 changed one file, P2AN006's own YAML companion, which was released with the note (P2AN006
v1.0.2). No other manual or app note declares it as a source, and the note it mirrors shipped in the
same push. **No document is flagged.**

## Impact survey — v1.24.5 (`release-yamls` §8, run 2026-10-12)

v1.24.5 reverses v1.24.4's silicon sweep (F-574). The 12 YAMLs are back to their pre-sweep served
text. `basic-io`'s one addition is a `source:` line, which the delivery filter strips. So every
manual's declared sources match what the manual was written against. **The v1.24.4 survey's
Assembly-manual re-audit flag below is withdrawn**: the KB again states the "(Rev B/C silicon)" and
"Rev C" framing the manual uses. **No document is flagged.**

## Impact survey — v1.24.4 (`release-yamls` §8, run 2026-10-12)

**What v1.24.4 changed:**
- The 130 OBEX objects became a pure catalog mirror. No document quotes the removed fields.
- 12 content YAMLs dropped their silicon-revision framing: GETCT ×2, `special_registers`,
  `serial_loader`, the errata status on AUGS/AUGD/SETQ blocks, GETXACC, the Goertzel page,
  `P_ADC_FLOAT`, `silicon_errata` and `basic-io`. Stephen, 2026-10-12: Rev C is the only P2 silicon.

**By manual:**
- **Declared sources:** P2AN001 and P2AN003 declare the ADC smart-pin page. Its only change is the
  `P_ADC_FLOAT` parenthetical, which neither note uses, so neither is affected.
- **Flagged: re-audit against HEAD, the P2 Assembly Language Manual.** Its opus-master states the
  same framing the KB dropped:
  - `special-registers.md:534`, `instructions-g.md:94,106` and `chapter-04-timing.md:545`: "64-bit
    counter (Rev B/C silicon)";
  - `appendix-j-known-bugs.md:86`: "affect all P2X8C4M64P Rev B/C silicon";
  - its `[Rev C]{.silicon-note}` markers, e.g. `appendix-e-constants.md:687`, a deliberate device of
    the manual (its CHANGELOG: "Rev C silicon notes").

  Whether that device stays is decided at the manual's re-audit; the KB side is done.
- **Not affected:** the P2 Errata's "confirmed on Rev C silicon by a test program" is a true record
  of what was run. The other "Rev B/C" hits are citations of the P2 Documentation's own title.

## Impact survey — v1.24.2 and v1.24.3 (`release-yamls` §8, run 2026-10-12)

Both releases changed the 130 OBEX objects only (catalog re-mirror, one-liners, `file_size` emptied,
`languages_confirmed` and `obex_version` removed; F-573). The one live document that names OBEX
objects is P2AN002 (#2811, #2812, #5278, #5361 in its text and Resources): its credits and claims
still hold against the mirrored data — "ersmith" is Eric R. Smith's handle (OBEX now lists the name),
and its titles differ from OBEX's only in punctuation and case ("FFT/IFFT" vs "FFT IFFT"). No manual
quotes an OBEX description, category or size. **No document is flagged.** Published state verified
live on p2kb-mcp 1.5.0.

## Impact survey — v1.24.1 (`release-yamls` §8, run 2026-10-11)

v1.24.1 changed one fact: `field` cannot name a method local (FIELD.yaml, CP-010). Every other hunk
moves provenance into stripped fields, removes pointers to material the KB does not have, or relocates
the OBEX upload date — no served fact changes. No live manual declares a local named `field` (grep of
every `opus-master/` for a PUB/PRI local list containing it: none). The Getting Started guide names
`jm_fullduplexserial` (OBEX 2842) in three `OBJ` shape examples (getting-started-body.md:342, 470, 746)
that illustrate block structure; none is in its compiled examples library, and the guide makes no claim
about the object, so the KB's removal of the compile verdict leaves it unaffected. **No document is
flagged.** Published state verified live on p2kb-mcp 1.5.0 (F-572 probes).

## Impact survey — v1.23.2 (`release-yamls` §8, run 2026-10-04)

v1.23.2 changed two facts, both decided on the bench (EF-090, EF-091). Sync serial TX primes its first
word in reset: the I/O & Smart Pins guide already teaches this (ch11:292-296), and F-533's fix text
carries it; no other live document teaches `%11100` ordering (the «#378» audit's per-document reads).
A `##` operand's AUGS takes a skip-pattern bit: the XBYTE guide already teaches it (xbyte-body.md:321-328);
the Assembly Reference states no skip-pattern AUGS rule («#378» G1: NOT-TAUGHT). **No document is
flagged.** Published state verified from raw.githubusercontent.com (both new sentences served); the
running p2kb-mcp needs a restart before F-526/F-540 can flip to `DONE`.

## Impact survey — v1.23.1 (`release-yamls` §8, run 2026-10-03)

v1.23.1 changed no fact: every edit moved a citation or a provenance key out of the shipped text
(F-523, F-400). No live document teaches a fact this release changed, so **no document is flagged.**
Published state verified from outside (raw.githubusercontent.com): `guides/pasm2-getting-started.yaml`
served = HEAD blob, sha256 = the published index entry, `v55:` shorthand absent. The running p2kb-mcp
refused it ("verification failed") — its boot-time index snapshot predates the release; F-523 and F-400
flip to `DONE` on the first served probe after an MCP restart.

## Impact survey — v1.23.0 (`release-yamls` §8, run 2026-10-03)

v1.23.0 changed facts (not only wording) in areas these live documents teach. Each flag is a
**re-audit-against-HEAD** signal for that document's next pass; the grep that located each
concrete site is the evidence, and the audit decides the fix.

| Document | What changed in the KB | Located in the manual |
|---|---|---|
| Architect's Guide | latest-wins mailbox handshake is load-bearing (F-507) | `architect-guide-body.md:919` states the disproven claim — **F-524** |
| P2AN007 | the re-check-the-sequence option is unsafe (F-521) | `P2AN007.md:214` (and the Tip below it) — owed under F-521 |
| Streamer Guide | GETXACC clears only during a Goertzel burst (F-506); streamer-DAC pin needs `P_CHANNEL` (F-513) | GETXACC: already open as F-479 |
| DEBUG Window Manual | SCOPE_XY DOTSIZE / SCOPE LINESIZE half-pixels (F-508); PLOT/MIDI COLOR, BITMAP SET, RATE un-freeze (F-516, F-518); DEBUG_TIMESTAMP stale-window caveat (F-514) | 6 files mention DOTSIZE/LINESIZE units — check each |
| I/O & Smart Pins | PINSTART Yval lost in trigger/serial modes (F-509); NCO Y = 0 (F-510); %10010 restart (F-511); DAC TT bit 0 (F-512); WRPIN pin-first (F-522) | no PINSTART-with-trigger-Yval site found (grep); the rest to the audit |
| P2AN003 | DAC smart-pin modes: OUT runs the ADC only with TT bit 0 (F-512) | to the audit |
| Assembly Reference | DEBUG_TIMESTAMP stale-window caveat (F-514); GETCT pair overhead (F-515, already stated as 2 in ch. 4) | 4 DEBUG_TIMESTAMP sites — check against the caveat |

No other live document's subject intersects the v1.23.0 fact changes; the F-519 id strip changes
no fact.

F-524 (the Architect's Guide mailbox claim) is DONE and archived — `correction-sweeps/2026-10-04-manual-releases-P2KB-CORRECTION-FINDINGS-archive.md`.

## Impact survey — v1.22.0 (`release-yamls` §8, run 2026-10-01)

The v1.22.0 delta (21 YAMLs: the P2 Errata silicon findings — `rdfast` + hub read/write family,
`setq`/`wmlong`/`setq_block_ops`, `augs`, `getct` + Spin2 `getct`/`getms`/`getsec`, `getxacc`,
`brk`, `muldiv64`, `wrpin`, `architecture/hub` and `smart_pins`) was intersected against every live
manual's declared sources, then each intersecting master was grepped for the statements the delta
contradicts (capture-and-clear GETXACC, conditional BRK, signed MULDIV64, `address & 7` slicing,
no-wait RDFAST use, GETSEC "long-duration").

- **Streamer Guide — DEFECT FOUND → F-479** (GETXACC capture-and-clear, §10.6 and §17.1).
- **Assembly Reference and deSilva — carried by «#352»** (its body names every entry: GETCT, GETXACC,
  RDFAST and the hub read/write family, SETQ, AUGS, BRK, Appendix J).
- **Architect Guide, Getting Started, I/O & Smart Pins, Single-Step Debugger, XBYTE — intersect, no
  contradicted statement found** by the targeted grep; re-audit against HEAD at each one's next pass
  (IOSP: the DAC-mode `TT` rule and §16.3's MULDIV64 ratio; Single-Step: its BRK material). XBYTE checked: every `RDFAST` it
  shows is `rdfast #0, …` — the waiting form — so E7 does not reach it.
- **No impact:** Debug Window, PNut-TS Terminal Guide. P2 Errata grounds on the silicon itself.

## Impact survey — v1.21.0 (`release-yamls` §8, run 2026-09-22)

The v1.21.0 delta (38 files: `hardware/`, `architecture/smart-pins|streamer|locks`,
`language/pasm2`, `language/spin2`, one app note) was intersected against every live manual's
`MANUAL-DESCRIPTOR.md` declared sources. **Two manuals intersect; eight do not.**

- **Assembly Reference — intersects `language/pasm2/`, `language/spin2/`, and is ALREADY ALIGNED.**
  Every flag-field correction this release shipped (`SUMC`/`SUMNC`/`SUMZ`/`SUMNZ` true-sign,
  `INCMOD`'s wrap, `RCR`'s shifted-out bit, `GETCT`'s WC-as-selector) was applied to the manual in
  «#348» *before* the YAML caught up, so the two trees now agree — verified in `appendix-a`
  (4 / 1 / 8 occurrences). **One row lags and is already recorded:** `LOC` moved to `category: Branch`
  here, and the manual still groups it under Arithmetic. That is on
  `workspace/p2-assembly-language-manual/PUNCH-LIST.md` with an expiry of the next Assembly release,
  including the note that Appendix C's per-category counts must be recomputed when the row moves.
  **No new flag needed.**
- **deSilva Tutorial — intersects `language/pasm2/`, `language/spin2/`; flag recorded here** because
  that manual has no punch list of its own. **Re-audit against HEAD at its next pass**, specifically
  for: the `SUM*`/`INCMOD`/`RCR` flag effects, `GETCT`'s WC (a selector, not a flag write), `LOC`'s
  category, and — most likely to bite a tutorial — the Spin2 `||` operator, which on P1 meant
  absolute value and on P2 means logical OR. A tutorial aimed at P1 refugees is exactly where that
  one does damage.
- **No impact:** Architect Guide, Debug Window, Getting Started, I/O & Smart Pins, Single-Step
  Debugger, Streamer Guide, XBYTE Guide, PNut-TS Terminal Guide. Recorded so the survey is visibly
  done rather than skipped.

## ✅ YAML-HEAD DRAIN GATE — evaluated 2026-09-22 («#351»): **GREEN**

The gate (`document-audit` §2) asks one question: are there **actionable** pending YAML corrections —
information not reaching the agents that consume this KB live? It had never been evaluated. All 61
open findings were classified, each **verified against the tree rather than read off its status**,
because the register lags reality and a stale `CONFIRMED` is indistinguishable from a live defect.

**Result: no actionable YAML correction remains open. The gate is GREEN.**

| Classification | n | Meaning |
|---|--:|---|
| **Landed this pass** | 13 | F-449, F-450, F-451, F-452, F-453, F-387, F-392(part), F-393, F-394, plus F-454…F-459 from «#350» |
| **Already done, status was lagging** | 8 | F-382, F-383, F-386(part), F-388, F-329, F-348, F-374, F-352 |
| **Blocked on external — parked, does NOT gate** | 7 | F-372, F-354, F-400, F-336, F-337, F-202, F-208 |
| **Not YAML — outside this gate's scope** | 15+ | tooling (F-405, F-439, F-376, F-389, F-381), ingestion (F-421, F-367, F-332, F-344, F-341), manuals (F-356, F-274, F-276, F-278, F-280, F-424, F-207, F-203, F-218), platform/PDF (F-316, F-317, F-300, F-301, F-299, F-319) |

**Why the parked set does not gate, individually:**
- **F-372** (`%11011` says a new WRPIN needs no reset, against the same document's general rule) —
  settles only on a bench: configure a USB pair, WRPIN with DIR high, observe. Jumper-only, so it is
  a *runnable* test, not an out-of-scope one. Class B periphery.
- **F-354** — six of eight items need an acquisition this repo does not hold (a level-shifter
  datasheet, ISP HUB75 driver docs, the #64013 and #64006 schematics, OBEX `psram.spin2` docs). Two
  of the eight have since resolved themselves via the HUB75 official-specs ingestion.
- **F-400** — a definition call on citation shorthand, Stephen's ruling. Worth knowing: expanding
  every shorthand is now **15 sites in 2 files**, not the 55 the entry was written against.
- **F-336, F-337, F-202, F-208** — bench or Chip Gracey. These are the hardware periphery.

⚠️ **Three things this pass proved about the register itself, which matter more than any single row:**
1. **Eight findings were already fixed and still read `CONFIRMED`.** A register whose statuses lag
   the tree invites re-chasing work that is done. Every row touched here was re-verified and flipped
   in the same pass.
2. **One finding's sub-claim was REFUTED** (F-394's C/Z entry condition, which is absent from the
   source it cites). A register entry is a claim like any other.
3. **`p2an006` cited `cogspin.yaml` for figures `cogspin.yaml` had no source for** (F-392). Two
   files agreeing is not provenance; it is a loop.

## The manuals were audited against the v1.18.0 delta at the FACT level, not the path level, and eight corrections were located that the path intersection could not see (2026-09-09, post-release manual sweep, applied 2026-09-10) — F-408…F-419

**How this surfaced.** `release-yamls` Step 8 recorded a **path intersection** — each document's
`MANUAL-DESCRIPTOR.md` declared sources against the release's changed files — and returned
*"INTERSECTS"* for 17 of 20 documents. Stephen asked for the list we would actually work from. A
path intersection cannot produce one: it says a document touches changed ground, never that it
restates a changed fact. Re-run at the fact level — 31 probes over all **126 live master files**,
every hit read in context — the answer is **9 documents with work and 7 with none**.

**Range extended to F-416 on 2026-09-10** as the sweep was applied: F-416 is a KB defect
(`cordic.yaml`) that this sweep *surfaced* rather than a manual correction, and it is kept under this
header because that is where its provenance is legible. **F-415 was rejected on the evidence** — see
its entry — so the header's "eight corrections" is seven applied plus one that was not a defect.

**Full located list, with the negatives that keep the sweep from re-deriving them:**
`engineering/analysis/2026-09-09-v1.18.0-manual-update-list.md`.

**Verified clean, so nothing below is a sweep target:** the `150 mA` per-pin scalar never reached
any manual (every drive figure reads 30 mA); no document carries TTL `VIL`/`VIH`/`VOL`/`VOH`
figures; ALM's interrupt vector map is correct (`$1F0=IJMP3` … `$1F5=IRET1`); `WRLUT` operand order
and LUT-sharing direction are both correct in ALM; `LOCKTRY` acquires everywhere; no fabricated
mnemonics (`RDCOGID`, `RDLUTS`, `NIXINT0`, `TRGINT0`) appear anywhere; no boot-ROM font or math-table
claim survives; no document states a `WAITMS` ceiling; and **of 95 shipped `examples-library/*.spin2`
files, none carries a pull idiom or a `-1` cog launch.**

### F-418 — the layout torture test is built on 44 constant names that exist in no Parallax source — `CONFIRMED` (scope decision owed)

`p2-layout-torture-test/opus-master/P2-Layout-Torture-Test.md`. Measured 2026-09-10 against **every**
ingested source under `engineering/ingestion/sources/` plus the published KB: of **63** `P_*`/`X_*`/
`EVENT_*` symbols the document uses, **19 are real and 44 appear nowhere**.

**Fixed in this pass (6 sites), because these claimed to be a symbol reference:**
- §6.2 *"Long Unbreakable Tokens"* — all three rows were invented at 30-32 characters. **The longest
  constant that actually exists in the P2 symbol set is 24 characters** (`X_2ADC8_16P_4DAC8_WFLONG`),
  so the section was calibrating the width allocator against an input no real document can produce,
  leaving the true worst case untested. That is a **validity** defect in the instrument, not a
  cosmetic one. Now the three longest real symbols (24 / 23 / 23), and `X_2ADC8_16P_4DAC8_WFLONG` is
  the right target for a second reason: it is the symbol that printed ON TOP of its own value in the
  released Assembly manual, the defect behind the tables filter's token-fit branch.
- §6.1 and two mode-table rows — `X_RFBYTE_1P_1ADC` / `X_RFBYTE_1P_1ADCb` → real analogues.
- Two **PASM2 code** sites — `xinit ##X_RFLONG_32P` → `X_RFLONG_32P_4DAC8`. A constant that does not
  exist inside a code listing is the least defensible instance of the class.

**Still open — 44 names, and it is a scope decision, not a defect to fix silently.** The rest sit in
the instrument's wide synthetic mode tables, whose cells are layout fodder ("HDMI and VGA framebuffer
scan-out"). The document is an **instrument**, never published to readers, and it is *"engineered to
reproduce every known layout defect"*. Against that, changing 44 symbols shifts column widths and
would invalidate the `VerifiedBox` claims throughout — each of which was verified against a specific
numbered render. **The question for the register's owner:** does the no-fabricated-names rule reach
an instrument's test fixtures, or stop at documents a reader can obtain? Answer that once and it
settles the whole table set; do not re-derive it per row.

**And F-356's own repair changed shape.** §1.24 settled that calling `P_HIGH_15K` a "15 kΩ pull-up"
is *acceptable vocabulary*; the KB stopped policing a word its own authority uses. What F-356 owes
is **the `DIR` caveat plus a source for the `P_HIGH_15K | P_LOW_FLOAT` composition**, not deletion of
the word. Anyone scoping F-356 off its original wording will do the wrong repair.

---


## Two same-named Silicon Doc DOCX copies disagree, and the KB garbled a flag semantic from that passage (2026-08-26, «#314» pre-flight) — F-367 · F-368 · F-369

### F-367 — `external-inputs/p2/` and `sources/silicon-doc/` hold DIFFERENT documents under the same filename — `CONFIRMED`

**How this surfaced.** «#314» went looking for a PASM2 DOCX and found `external-inputs/p2/` holds
DOCX originals for several sources — **including a second copy of the Silicon Doc**, same filename,
different size (4,919,444 vs 4,814,991 bytes).

**Measured, not assumed.** Both carry 48 tables and 34 media, so a structural check calls them
identical. Extracting text from each and diffing says otherwise: **972 characters differ across 4
sites.**

| Site | `sources/` (the copy used for the 2026-08-26 re-extraction) | `external-inputs/` |
|---|---|---|
| GETBRK WZ | `Z = 1 if no … pattern queued (D = 0) or **0** if pattern queued (D <> 0)` | `… or **1** if pattern queued (D <> 0)` |
| smart-pin reset | **carries a full paragraph**: *"Once a smart pin is configured via WRPIN and then started by making its DIR bit high, it can be reset at any time by making its DIR bit low. It does not lose its configuration…"* | **paragraph absent** |
| PWM dither rationale | *"a maximum of only two adjacent 8-bit DAC levels are set for every 2…"* | *"a maximum of only two transitions occur for every 256 clocks"* |
| typo | `cog regis+ters:` | `cog registers:` |

**Which is right, and why it is decidable without a third source.** The `external-inputs/` GETBRK
line sets **Z = 1 in both branches**, which makes `WZ` useless and cannot be what the silicon does;
`sources/` gives `Z = 1 / Z = 0`, which is also the conventional Z semantic (`D = 0 → Z = 1`).
**The copy used for the re-extraction is the correct one**, and it additionally carries a paragraph
the other lacks. No prior work is invalidated.

**Why it still matters.** Two files with one name, differing on a flag semantic, is a silent
corruption waiting for whoever opens the wrong one. `external-inputs/p2/` is not a source folder and
carries no dashboard row, no audit and no trust tier — it is a staging area that has quietly become
a second, unlabelled copy of the corpus. **Disposition is Stephen's:** label `external-inputs/p2/`
as staging-only with a pointer to the canonical `sources/` copies, or reconcile the copies. Recorded
as **needs Stephen's accept-or-fix**.

**Also found there and NOT blocked as previously reported:** `Propeller 2 Questions & Answers.xlsx`
— the `p2-qa-spreadsheet` row sits at 80% and was listed in this sprint's plan as having *no primary
document staged*. It has one. That plan line is wrong and is corrected in «#318».

---
## Carry-forward guardrails — investigated and settled; do NOT re-file (full detail in the archive)

- **F-002 (`WONTFIX`):** `?` / `||` operator-form failures were an agent usage error — the KB is correct (`??var` = XORO32 random; `ABS()` not `||`; `?` is the ternary operator).
- **F-036 (`WONTFIX`):** `calld.yaml` — LOC loading a 20-bit address into PA/PB/PTRA/PTRB is not a defect.
- **F-093 (`WONTFIX`):** `lockrel.yaml` C-flag polarity — the appendix's "inverted" claim is the error; the YAML is correct (C = lock-was-held).
- **F-114b (`RESOLVED-INVALID`):** the MIDI display modes KEYBOARD / GRID / ROLL / MONITOR do **not** exist in PNut v55 — do **not** add them to `midi.yaml` (it carries an explicit `not_supported:` claim).
- **Verified-resolved (don't re-chase):** the Jan-2026 streamer KB audit's issues were all reconciled in the 2026-05/06 passes (DAC routing, 32-pin groups, mode encoding, xcont/xzero phase wording, setxfrq 2³¹ formula, streamer symbols). Only the XZERO concept text was open and is fixed (F-003).

---

## Five defects surfaced while ending the drive-strength mislabel class (2026-08-25, «#296» §5) — F-342…F-346

> **Origin.** All five were found while correcting F-321…F-324 — three of them only because
> R8 forces a **semantic read** of every example after it compiles. Three are fixed in that same
> pass and marked so; two are not this task's repair and are filed for the head that owns them.
> Every line number below was read off disk on 2026-08-25.

### F-344 — the derived board extract contradicts itself in one sentence about switch polarity — `CONFIRMED`
> **KB decision:** not KB: the derived extract in the ingestion tree

> **Where:** `engineering/ingestion/sources/p2-eval-add-on-boards/boards/addon-control-64006a.md:9-11`
> — *"each **active-high** push-button has a **470 Ω series resistor** so the I/O pin is **driven
> low** while the button is asserted."*
>
> **Active-high and driven-low-when-asserted cannot both be true of the same switch.** The rest of
> that same file says active high in the pin map (`:20-23`), and the shipped
> `hardware/addon-control-board.yaml:16-20` says *"the I/O pin reads high while the button is
> pressed"* — so the KB already resolved it the other way. The extract's own summary sentence is
> the outlier.
>
> **Ingestion-tree defect, not a YAML edit** — this file is derived source-research and is frozen
> to KB maintenance. Same class as **F-341** (our own derived documents inside the truth root).
> **What is owed:** re-read the #64006A Product Guide v2.0 page and correct the extract's summary
> sentence, or record why the guide itself says both.

---

## `hardware/` repopulated from the board guides — the return record, and the wrong scalars the source-first read exposed (2026-08-25, «#307» Plan §8 part 2) — F-353 · F-354

> **Origin.** «#294» removed 59 quantitative blocks from `deliverables/ai/P2/hardware/` (F-334, two
> records: 48/16 files and 11/6 files). «#298» dispositioned every one. «#307» worked the **board
> guides**, not the removal list, and wrote back what each guide states. One of the 11 —
> `language/spin2/methods/getct.yaml description` — is outside this tree and belongs to «#299», so
> **58** were in scope here. Every line number below was read off disk 2026-08-25.

### F-354 — eight content-level holes in the repopulated `hardware/` blocks: seven are closed or applied (the five driver-shaped ones by removal 2026-10-07; the PCB dimensions and the `addon-serial-device` supply 2026-10-10, «#420»), and one is BLOCKED on a document this repo does not hold (the #64013 schematic) — `PARTIAL`
> **KB decision:** held (document): the #64013 RTC schematic; `addon-rtc.yaml` carries a gap note meanwhile

> **Why these are not "gaps" in the three-number sense.** Every ACTIONABLE block returned. What did
> not return is *material inside* those blocks — figures the KB shipped that no ingested source
> states. Each open one is recorded in the YAML itself, at the point of use, with what would settle
> it, so a reader meets the hole where the fact would have been.
>
> **Re-scoped 2026-10-07 by Stephen's ruling** (he designed the HUB75 adapter): *"it is best that
> we do not get too specific about the driver so we don't have to update every thing the driver
> changes.. the api matters to code, the pinout matters to code."* A hardware entry carries the board
> — pinout, pin budget, voltages, level shifting, the board's published ceiling — and names its
> driver; the driver's timings, chain counts, cog use and chipset table are the driver's, and the
> v4 HUB75 driver is coming. So a driver-shaped hole is closed by **removing the hole**, not by
> sourcing the number (`.claude/doctrine-overlay.md`, *A hardware entry carries the board, not the
> driver that runs it*). The entry previously said six of the eight needed documents this repo does
> not hold; that was also wrong for the HUB75 rows — Stephen's driver repository is in
> `engineering/ingestion/external-inputs/source-code/external-projects/p2-HUB75-LED-Matrix-Driver/`
> (`THEOPS.md:149` states 1–3 adapters; nothing under `driver/` uses the streamer).
>
> | Hole | Disposition |
> |---|---|
> | HUB75 max clock **40/35 MHz**, **13 ns** | **CLOSED 2026-10-07.** Board fact, already sourced: the designer's spec says 70 MHz, limited by the 2x 74HCT244 (`p2-hub75-adapter-official-specs.md:22`). `gap_max_clock` deleted; `specifications.electrical.panel_clock_note` added from the designer's own note (HUB75Adapter.md "Specifications" note: the panel's chipset sets the clock, far below the adapter's ceiling). No datasheet needed. |
> | HUB75 **pulse-width minimums**, 3/8-bit refresh table | **CLOSED 2026-10-07 — driver facts, out of scope.** `gap_pulse_widths` deleted with the rest of the driver restatement in `software_features` (feature list incl. a wrong "automatic panel detection" — the driver is configured per panel chipset — refresh rates, bandwidth model); replaced by a pointer to OBEX 2850. |
> | HUB75 **"maximum 3 chains"**, **"no streamer"** | **CLOSED 2026-10-07 — driver facts, out of scope.** `notes.gap_chain_limit` deleted. The `led_driver_chips` table (the driver's per-chipset configuration) removed for the same reason. |
> | HUB75 **board current 35 mA**, per-panel currents | **CLOSED (verified 2026-10-07).** The board's own draw ships sourced (`specifications.electrical.board_consumption`, "under 50 mA", `official-specs.md:126`); the held `power_requirements` block is gone from the tree; panel currents are the panel's. |
> | **"One cog consumed by the PSRAM driver"** (32 MB module) | **CLOSED 2026-10-07 — driver fact, out of scope.** The `(uses 1 cog)` comment removed from `code_patterns.spin2.obex_driver_usage`. The rest of that file's driver restatement (`code_patterns`, `protocol_constraints` driver settings) is the class sweep **F-548**. |
> | Whether the **#64013 RTC board carries its own SDA/SCL pull-ups** | **OPEN** — `addon-rtc.yaml` `pin_mode_tip.scl_pull_up_caveat`. A board fact that changes how it is connected. Needs the #64013 schematic (referenced by the guide, not ingested). **BLOCKED — missing document, re-checked 2026-10-10 («#420»):** `sources/P2-RTC-Add-on/` holds the guide, the PCF8523 datasheet and the example archive, no schematic. The page asserts nothing about pull-ups (it says in so many words that neither the guide nor any ingested source states it), so there is no claim to remove. **Stephen / ingestion:** obtain and ingest the #64013 schematic from the 64013 product page (www.parallax.com, search 64013). |
> | Numeric **PCB dimensions for the #64006 add-on boards** | **CLOSED 2026-10-10 («#420»).** Read off the guide's PCB Dimensions drawings (pp.11-12, rendered): A/V 3.2 x 1.3 in, Goertzel 3.2 x 1.2 in, small modules 1.6 x 0.8 in (drawn for the LED Matrix). `addon-goertzel-touch.yaml` `specifications.pcb_size_class` replaced by `pcb_size` (3.2 x 1.2 in, 81.3 x 30.5 mm) and the contradicting `size_class: small_addon` → `medium_addon`. The other small boards inherit the guide's "small modules" grouping; no per-board dimensions are stated for them and none were set. |
> | `addon-serial-device.yaml` **"3.3 V supply"** | **APPLIED 2026-10-09/10 («#413», «#420»)** — the unsourced voltage and `power_sharing` lines are removed and the page states no supply, per Stephen's Q7 (study decisions, 2026-10-09): the Rev B ACC HDR/5V shunt jumper is an Eval-board fact that matters for any add-on using header 5 V, already modelled on `p2-hardware-feature-comparison.yaml` and `addon-serial-host.yaml`; no erratum. (A `power_note` added in «#420» restating the guide's Serial Host vs Revision History wording was removed by the arbiter as contrary to Q7.) |
>
> Status: `PARTIAL` — seven closed or applied (they ship in the next KB release, `PENDING-VALIDATION`);
> one blocked: the #64013 schematic is not ingested (Stephen / ingestion: obtain it from the 64013 product page).

---

## WRPIN D-operand field map: three field descriptions wrong in the YAML, ten mode numbers footnote-fused in an ingestion artifact (2026-08-24, `KNOWLEDGE-GAPS` pass-6 catch-up) — F-331, F-332

> **Origin.** The pass-6 gap-ledger catch-up read the WRPIN bit-field map in both 2026-08-24
> repaired captures (P2 Datasheet pp.23-25, P2 Hardware Manual Tables 16-25) to close
> `KNOWLEDGE-GAPS.md` **G-001** and **G-008**. Both defects below were found while doing that
> reading. **Nothing is fixed in this filing.**

### F-332 — the P2 Hardware Manual's table artifact carries ten six-digit `%SSSSS` values for a five-bit field, with no reconciliation note — `CONFIRMED`
> **KB decision:** not KB: the table artifact in the ingestion tree

**Location:** `engineering/ingestion/sources/p2-hardware-manual/complete-tables-reference.md:287-314`
(Table 25) and the same table in
`engineering/ingestion/sources/p2-hardware-manual/p2-hardware-manual-text.txt:1030-1036, 1053, 1054, 1056`.

**Ten values, each a 5-bit mode with its superscript footnote `¹` fused on:** `001001` `001011`
`001101` `001111` `010001` `010011` `010101` `110111` `111001` `111101` — correctly
`%00100¹` `%00101¹` `%00110¹` `%00111¹` `%01000¹` `%01001¹` `%01010¹` `%11011¹` `%11100¹`
`%11110¹`, footnote 1 being *"OUT signal overridden"* (the artifact carries that footnote
immediately below the table).

**This is a known, already-adjudicated class — and the adjudication is in the wrong file.** The
`p2-datasheet` artifact names the identical defect as reconciliations **R1** and **R2**
(`sources/p2-datasheet/complete-tables-reference.md:49-50`), decided by three of four extraction
paths plus a visual read of the rendered pp.34-35, and its **R8** even records that "The Hardware
Manual's DOCX (Table 9) carries the identical fusion, so this reconciliation applies to both
sources" — for Table 9's `INA`/`INB` only. **No such note exists anywhere in the Hardware
Manual's own artifact** (a case-insensitive search of that file for *footnote*, *superscript*,
*reconcil*, and *OUT signal overridden* returns nothing).

**KB impact: NONE today — recorded so it stays that way.** No fused value reached
`deliverables/ai/P2/` (grepped for all ten; the only near-hits are COGINIT mode bits in
`spin2/patterns/implementation/spin2_cog_management.yaml`, unrelated). The exposure is forward:
an agent deriving smart-pin YAML from the Hardware Manual artifact alone gets `%001001` for
pulse/cycle output.

**Proposed correction (ingestion head, not a YAML edit):** add the R1/R2 reconciliation note to
`sources/p2-hardware-manual/complete-tables-reference.md` beside Table 25, in the form the
datasheet artifact already uses. **Wider question worth one pass:** the DOCX walk drops
superscript markers into the adjacent numeral generally — Table 9's `INA1`/`INB2` is the same
mechanism, so Table 25 is unlikely to be the only other instance.

---


## Six defects surfaced while building the single constant-definition home (2026-08-25, «#295» phase 2) — F-341 (F-336 … F-340 archived)

> **Origin.** All six were found while implementing «#295» — promoting the drive ladder into the
> KB and collapsing two `P_*` definition homes into one. Two are fixed in that same pass and are
> marked so; four are not this task's repair and are filed for the task that owns them. Every
> number below was measured against disk on 2026-08-25, not carried from the design.

### F-341 — six of our own derived analysis documents sit at the root of `engineering/ingestion/sources/`, repeat the pull-up mislabel F-321 exists to kill, and are inside the fidelity gate's declared *Parallax documentary* truth root — `PARTIAL`
> **KB decision:** not KB: the derived analysis files in the ingestion tree

> 🔴 **F-341 IS SHARPER THAN "LATENT" — THOSE FILES INVENT PARALLAX PART NUMBERS. Confirmed by
> Stephen 2026-08-26.**
>
> Asked whether our board coverage was complete, the inventory turned up three part numbers with
> **zero occurrences in any ingested source directory** — i.e. in any actual captured Parallax
> document. They exist only in the loose analysis files at `engineering/ingestion/sources/`:
>
> | Invented | Where it appears | What it actually is |
> |---|---|---|
> | **#64025 "LED Board"** | `p2-hardware-validation-checklist.md:102`, `p2-board-power-analysis-matrix.md` | **does not exist** — the real board is **#64006C LED Matrix** |
> | **#64026 "7-Segment Display"** | `p2-hardware-validation-checklist.md:150` | **does not exist** |
> | **#64027 "Switches Board"** | `p2-hardware-validation-checklist.md:191` | **does not exist** — switches are on the **#64006A Control** add-on |
>
> **Stephen, asked directly: "LED board, no. 7-segment, no. Switches, no."**
>
> **Why this is worse than a wrong name.** The inventions are *plausible* — they describe real
> capabilities (LEDs, a display, switches) that map onto real boards, at part numbers adjacent to
> the real #64019/#64020/#64029 range. And `#64027`'s validation section is headed **"Test 1:
> Pull-up Test"**, so the fabricated board carries the fabricated mechanism. A reader has nothing to
> catch it with.
>
> **None of the four files names a Parallax document anywhere.** Their headers are
> *"Comprehensive testing procedures…"*, *"Complete power budget calculations…"*, *"Complete
> cross-reference for automatic code generation"* — authored analysis, with no provenance, sitting
> in the directory reserved for captured sources. **Location is doing the work of attribution.**
>
> 🟢 **CONTAINMENT VERIFIED: zero leakage.** `grep -rl` for all three across `deliverables/ai/P2/`
> returns **0 files**. The shipped KB never carried them, and «#305» had already excluded loose
> root files from the fidelity tool's truth side. The damage is confined to the ingestion tree.
>
> **Still open, and it is a scope call:** the four files remain where sources live, they still assert
> the pull-up mislabel, and the compatibility/power matrices cross-reference boards that do not
> exist — so anything derived from them is derived from fiction. Options: correct them in place and
> relabel as analysis, relocate them out of `sources/`, or retire them. **Not actioned pending
> Stephen's decision.**
>
> 🟢 **THE INVENTED-PART-NUMBER HALF IS CLOSED 2026-08-26 («#323»).** Stephen's standing rule —
> *"no fabricated names in the KB tree, delete invalid names outright"* — settled the disposition
> without needing a further decision, so it was executed. **Every `#64025` / `#64026` / `#64027`
> site in the repository was worked**, which was more than the three the finding names:
>
> | File | What was there | What was done |
> |---|---|---|
> | `sources/p2-hardware-validation-checklist.md` | three validation sections (`:102`, `:150`, `:191`), incl. the `#64027` "Pull-up Test" that carries the F-321 mislabel | sections deleted, dated removal note left in place |
> | `sources/p2-board-power-analysis-matrix.md` | three power-analysis sections, two `case` arms in worked code, five Quick-Reference rows | all deleted, removal note left |
> | `sources/p2-complete-signal-flow-matrix.md` | three signal-path sections, a VIO-load `case`, three `ADDON_*` constants, an impedance-detect routine returning two of the invented boards | all deleted, removal note left |
> | `sources/p2-board-addon-compatibility-matrix.md` | three grid rows, five detailed configurations across two boards, three power rows, three `case` arms | all deleted, removal notes left |
> | `plans/quick-bytes-ingestion-plan.md` | `parallax_id: "64025"` against **"P2 RTC Add-on Board"** | **corrected to `64013`** — the real part number, from `sources/edge-breakout-board/edge-breakout-board-narrative.txt:137` |
> | `knowledge-base/P2-support/extractors/hardware-specs-extractor.py` | a YAML **generator** with all three baked in, emitting them under `source: P2 Documentation Collection` | the three entries deleted, note left |
>
> **Deleted rather than relabelled, deliberately.** The nearest real boards are the **#64006C LED
> Matrix** (an 8×7 Charlieplexed grid driven on 8 pins) and the **#64006A Control** add-on (four
> buttons and four LEDs); there is no 7-segment board in the #64006 series at all. The removed pin
> maps, currents and test procedures described none of those, so relabelling would have attached
> fabricated numbers to real boards — a worse defect than the one being fixed.
>
> After: `grep -rn '64025\|64026\|64027'` across the repository returns **no hit that presents a
> board**. Every surviving occurrence is one of four kinds: a dated removal note at the site the
> content was cut from, the `#64013` correction comment, the sprint plan's task row, or this
> register's own documentation above. Deliberately stated as classes rather than a count — the
> count changes every time this register is edited, and a self-referential tally is stale the
> moment it is written. (Arbiter check, «#323»: the figure first written here was 11; the live
> number was already 15, because writing the table above added hits to the thing being counted.)
>
> **Two halves remain open**, both unchanged by this pass: the four files still sit at
> `sources/` top level asserting the pull-up mislabel (the relocate-or-repair-or-retire call), and
> the *same class* of unverified part numbers survives in them — `#64028` "Buttons Board",
> `#64029` relabelled "Switches and LEDs Combo", `#40003` "Protoboard", `#40007` "Digital I/O
> Board". Those four were left strictly alone because Stephen confirmed three numbers, not seven,
> and «#323» would have been widening its own scope to act on them.

> 🔴 **THE LATENT DISARM WENT ACTIVE, EXACTLY AS THIS FINDING PREDICTED — and is now closed
> at the instrument (2026-08-25, «#305»).** This entry says the disarm is "a shape away, not a
> policy away". «#305» changed the shape (the harvest had to read the current-edition v55
> table, whose rows put the name in column 2), and with the repaired parser and no guard,
> `p2-complete-signal-flow-matrix.md:100` — a **signal-flow** table whose last cell happens to
> hold a constant name — defined `P_PWM_SAWTOOTH` as **"P38"**, the pin number in the
> neighbouring cell. One of our own derived documents teaching the instrument our own
> inference, in the first run after the shape changed.
>
> **Closed structurally, not by a list of six names.** An ingested source **is a directory**:
> every real source under `sources/` lives in its own folder because that is what the ingestion
> process creates, so a loose file at the root of a truth root was put there by something else
> and is not an ingested source document (`MIN_DEPTH_BELOW_ROOT`). That rule excludes all
> **twelve** loose files at `sources/` top level, not just these six, and it catches the next
> stray file without an edit. A second, independent guard bounds the name cell to the first two
> columns — a constant in the last column is a *use*, not a definition. Both carry negative
> controls, including the exact `P_PWM_SAWTOOTH | P38` row.
>
> **`TRUTH_ROOTS` was NOT widened or narrowed** — the roots are unchanged; only what counts as
> a file inside them is now defined.
>
> **Still open, and it is the half this finding actually asked for:** the six documents remain
> at `sources/` top level, still asserting a 15 kΩ internal pull-up the P2 does not have. The
> instrument can no longer be misled by them; a reader still can. Relocating them to a derived/
> analysis area, or repairing them against the Datasheet legend, is unchanged and unowned.
>
> Status: `PARTIAL` — instrument disarm closed and controlled; the invented-part-number half
> is closed at every site in the repository (2026-08-26, «#323» — see the boxed note under
> F-356); the content relocation, and the four further unverified part numbers those files
> carry (#64028, #64029-as-combo, #40003, #40007), are owed.

> **The six**, all at `engineering/ingestion/sources/` top level, all self-describing as
> generated cross-references rather than Parallax publications:
> `p2-board-addon-compatibility-matrix.md` · `p2-complete-signal-flow-matrix.md` ·
> `p2-hardware-validation-checklist.md` · `p2-board-power-analysis-matrix.md` ·
> `p2-board-pin-mapping-knowledge.md` · `p2-addon-board-circuit-knowledge.md`.
> Their own subtitles give them away — *"Complete cross-reference for automatic code generation"*,
> *"Comprehensive testing procedures"*, *"Knowledge Base"*. No Parallax document is named on any
> of them.
>
> **What they assert.** The F-321 mislabel, verbatim and repeatedly:
> `p2-complete-signal-flow-matrix.md:127` *"WRPIN(pin, P_HIGH_15K) ' 15kΩ pull-up"*, `:62`
> *"Input Type: Digital with internal pull-up"*, `:65` *"220µA through pull-up when pressed"*;
> `p2-board-power-analysis-matrix.md:79` *"Internal pull-up: 15kΩ to 3.3V"*;
> `p2-board-addon-compatibility-matrix.md:84` *"8 × 220µA pull-up current = 1.76mA"*;
> `p2-hardware-validation-checklist.md:198` *"Enable internal pull-ups"*. The P2 has no such
> component — `P_HIGH_15K` selects **drive strength**, per the Datasheet p.24 Pin Mode Legend
> (`p2-datasheet-text.txt:1139-1147`). The 220 µA and 1.76 mA figures are stated by no Parallax
> source.
>
> **Why it is more than stale prose.** `audit-constant-fidelity.py` scopes its truth side to
> `TRUTH_ROOTS = [ingestion/sources, ingestion/smart-pins-catalog]` with a comment explaining that
> an unauthoritative source does not add a wrong answer, it **DISARMS the check** — that is why
> `external-inputs/` was excluded. These six are unauthoritative and are *inside* the root.
> **Measured today: they contribute 0 entries to the truth table**, because their pull-up lines do
> not happen to match `ROW_RE` or `BULLET_RE`. The disarm is latent, not active — a shape away, not
> a policy away.
>
> **What is owed.** Decide what these files are and put them where that is true: relocate to a
> derived/analysis area outside `sources/`, or repair them against the Datasheet legend and label
> their provenance. Either way they must stop reading as Parallax documentary sources.
> **Same class as the arbiter's F-322 correction** — a derived extract inside the ingestion tree
> mistaken for the source it was derived from. Two instances in two days makes it a class, not an
> accident: an audit of what actually lives under `ingestion/sources/` is owed.

---

## An ADC comparator example still states the input threshold in fixed volts, in the manual F-412 just repaired (2026-09-11) — F-424

### F-424 — IOSP §2.5's ADC comparator example quotes `~1.65V` as an input threshold without the supply-fraction caveat the same manual now carries everywhere else — `CONFIRMED`

Found 2026-09-11 while **validating F-412 on the released PDF** — which is the point worth
recording: the validation pass for one finding is where the residual sites of its class surface,
because it is the only pass that reads the whole artifact looking for that exact shape.

`P2-IO-and-Smart-Pins-User-Guide.pdf` **page 59** (§2.5 ADC modes), in the worked example:

```
' Detect when analog input exceeds ~1.65V (mid-scale)
WRPIN(adc_pin, P_ADC_1X)
PINFLOAT(adc_pin)
```

**Why this is the F-412 class and not a duplicate of it.** F-412 named
`chapter-12-digital-input.md:25` and `:95` and was repaired there — p184 now states the threshold
as a fraction of `Vxxyy` (0.3 / 0.5 / 0.7), calls it a band rather than a point, and ends
*"Quote 1.65 V as the typical value at 3.3 V, never as the switching point."* This site is a
**different chapter** and states a comparator trip point as a fixed voltage with no supply
reference at all. `(mid-scale)` carries the fraction implicitly for a reader who already knows
the rule; the reader who meets this page first does not.

**It is genuinely wrong off-nominal, which is what makes it a finding rather than a style note.**
`Vxxyy` is specified 3.15 V - 3.45 V, so mid-scale spans roughly 1.58 V - 1.73 V, and pin groups
on different supplies do not share a threshold. The manual states this itself at p184 and again at
p187 (*"the fraction is what the level fixes"*) and p195 (*"Levels below assume Vxxyy = 3.3V;
scale them to your I/O supply"*) — three sites carry the caveat and this one does not.

**Fix.** One line, in
`engineering/document-production/workspace/p2-io-and-smart-pins-user-guide/opus-master/` §2.5:
state the trip point as mid-supply and give 1.65 V as the value at a nominal 3.3 V, matching the
vocabulary p184 already established. Do not delete the number — the reader needs a figure to
aim at; it needs the supply attached to it.

**Class sweep owed with the fix** (`feedback_classwide_sweep_on_every_finding`): re-read every
site in the IOSP that names an input threshold or comparator trip point in volts and confirm each
carries the supply. This entry records only the site the F-412 validation pass happened to cross.

---

## YAML→Manual impact survey — KB v1.16.3 (2026-08-16, `release-yamls` §8)

Delta: `spin2/methods/wrpin.yaml` · `architecture/smart_pins.yaml` ·
`architecture/smart-pins/smart-pin-11011-usb-host-device.yaml` · `architecture/cordic.yaml` ·
`architecture/streamer/overview.yaml` · `architecture/streamer/dds-goertzel.yaml` ·
`pasm2/getxacc.yaml` · `spin2/integration/spin2-pasm2-integration.yaml` ·
`spin2/special-symbols/at.yaml`.

Intersected against every live manual's `MANUAL-DESCRIPTOR.md` declared sources. **Survey done, not
skipped.** Most intersections are already owned by an in-flight Sprint 2 task, so no duplicate flag
is raised for them; the ones that are **not** covered are flagged below.

| Element | Intersects on | Disposition |
|---|---|---|
| Streamer Guide | streamer, dds-goertzel, getxacc, DEBUG_COGS | **covered** — «#220» «#221» |
| IOSP | `architecture/smart-pins/`, smart_pins | **covered** — «#219» (and the F-264 %TT material rides its v1.0.9 pass) |
| Assembly Reference | cordic, streamer | **covered** — «#228» |
| P2AN002 | cordic | **covered** — «#236» |
| XBYTE Guide | streamer | **covered** — «#227» (§15.3 restructure); see the F-268 flag below |
| **P2AN001 / P2AN003** | wrpin | **⚑ FLAG — re-audit against v1.16.3.** These two were read site-by-site and taken OUT of the release wave, but that read answered **F-259's** question (does every executable example carry `\| P_OE`?). **F-264 is a different fact** — that `%TT` is context-dependent and that adding `P_OE`/`P_CHANNEL` to a **non-smart-pin cog DAC** kills it. Any cog-DAC or `P_DAC_*` configuration in these app notes was never checked against that. Do not treat the wave exclusion as covering it. |
| **P2AN004** | wrpin | **⚑ FLAG — same class as above**, and it was never in the wave at all. |
| **Architect's Guide** | CORDIC, streamer | **⚑ FLAG — re-audit against v1.16.3.** Not in the release wave. Declares both sources; the CORDIC hub-in-loop rule (F-263) and the `DEBUG_COGS` streamer caveat (F-266) are new since its last pass. |
| **DeSilva Tutorial** | CORDIC | **⚑ FLAG — re-audit against v1.16.3.** It *is* in the wave, but for §1/§2 (Acknowledgments, Appendix A) only — its CORDIC material is untouched by «#222»/«#223» and unexamined against F-263. |
| All elements showing PASM fragments | `spin2-pasm2-integration.yaml` | **⚑ FLAG — F-268 class sweep**, filed below and deliberately not folded into a correction task. |

These flags are the drift signal `document-audit` drains on each element's next pass. They are
**not** Sprint 2 scope and must not be pulled into it silently — surface them to Stephen as a scope
decision.

---

## Stephen's review of the Sprint 2 gate release (2026-08-16, «#234») — F-276…F-283

> **Full dispositions and reasoning:** `engineering/planning/SPRINT2-VISUAL-REVIEW-NOTES-2026-08-16.md`.
> Eight observations (V-1…V-8) worked one at a time against the gate commit `fea28f1c`. Four became
> findings; the rest were scope and structure decisions recorded in that file.
>
> **All four are tasked into the voice-conformance family «#240»–«#248» and are absorbed into the
> per-manual pass rather than applied as point fixes** — applying them first and conformance-checking
> after would write the same prose twice and have the second pass judge what the first just wrote.
>
> **Two of these were found by the review, not by the sprint's own sweeps**, and that is the useful
> part: F-277's site sits in body text no Sprint 2 task touched. A findings-driven sweep sees the
> diff; it does not see the document.

### F-280 — `pnut_ts` survives in 16 masters as a command that does not run. `PARTIAL — the whole declared sweep APPLIED in opus-master 2026-08-25 («#301»); publication owed, per document`

**Found:** 2026-08-17 during the P2AN001/P2AN002 voice pass («#247»), by checking the compiler name
the two notes hand the reader against the name of the binary that exists.

**This was already adjudicated and only half-swept.** Commit `c203fa52` (2026-08-11) established the
finding on its merits: `command -v pnut_ts` finds nothing, the installed binary is `pnut-ts`, and the
tool's own usage banner reads *"PNut-TS: Usage: pnut-ts [optons] filename"*. SSDB and the PNut-Term-TS
guide were corrected then — 21 sites — and both voice guides were amended so it could not come back.
**The rest of the set was never swept.** Thirty-three occurrences remain across eighteen files, against
thirty-nine correct ones — a near-even split, so the set currently teaches both.

**Fixed in this pass (2 sites, the two notes being touched):** `P2AN001/opus-master/CHANGELOG.md:37`
and `P2AN002/opus-master/CHANGELOG.md:35`. Both are reader-facing — an app-note CHANGELOG is promoted
to the published `p2anNNN-changelog.md` beside its PDF.

**Remaining (31 sites, 16 files) — the class-wide sweep this finding owns:**

| Element | Sites |
|---|---|
| Getting Started Guide | `getting-started-body.md` ×1 — **highest reader risk**: a beginner's first compile |
| Architect's Guide | `architect-guide-body.md` ×1, `CHANGELOG.md` ×2 |
| ~~Assembly Language Manual~~ | ~~`CHANGELOG.md` ×1~~ — **CLEAR, verified 2026-08-22**: `pnut_ts` appears nowhere in `opus-master/`. (Its three *process* docs carried 10 tool-invocation uses; corrected the same day. The remaining hits in `audit/`, `archive/` and `code-validation/` are frozen records, and `external-inputs/pnut_ts_facts/` is a real path — all correctly left alone.) |
| PNut-Term-TS Guide | `CHANGELOG.md` ×1 (the body was swept at `c203fa52`; its CHANGELOG was missed) |
| deSilva | `archived-2025/README-COMBINED-MASTER.md` ×3 — **archived scaffolding, not shipped; excluded** |
| P2AN003 – P2AN007 | body ×17, `CHANGELOG.md` ×5 |

**Not swept here on purpose.** Conform-on-touch: these elements are not being touched by Sprint 2, and
pulling sixteen masters into a voice pass is the big-bang sweep the rule exists to avoid. Each takes it
at its next visit — this row is what makes sure the visit knows.

**The correction is one substitution** — `pnut_ts` → `pnut-ts` — with no prose consequence. Check each
site is the *command*; the project name in running text is properly **PNut-TS**.

> **SWEEP APPLIED 2026-08-25 («#301»). The conform-on-touch deferral above is discharged: the visit
> came.** All 27 reader-facing occurrences substituted across **14 files**, line counts unchanged
> (4,907 before and after), diff is exactly 27 insertions / 27 deletions.
>
> **⚠️ The row header's own arithmetic was wrong, and re-measuring it is how the extra defect turned
> up.** It reads *"Remaining (31 sites, 16 files)"*; the table under it sums to **30 sites / 15
> files**, because the `~~Assembly Language Manual~~ CHANGELOG ×1` row was struck through as CLEAR on
> 2026-08-22 and the header was never re-totalled. Measured on disk today: **30** occurrences across
> **15** files under `opus-master/`, of which **3** in **1** file are the excluded deSilva
> `archived-2025/README-COMBINED-MASTER.md` — leaving **27 in 14**, which is what was fixed. The
> table's per-element counts were all correct: Getting Started ×1, Architect body ×1 + CHANGELOG ×2,
> PNut-Term-TS CHANGELOG ×1, P2AN003–007 body ×17 + CHANGELOG ×5.
>
> **A second wrong name rode along on one of the lines, and is fixed with it.**
> `pnut-term-ts-user-guide/opus-master/CHANGELOG.md:106` carried *"`pnut_ts` + `pnut_term_ts`"* —
> **both** underscore forms, in the guide whose own `MANUAL-DESCRIPTOR.md:28` and `voice-guide.md:83`
> declare *"the underscore forms `pnut_ts` / `pnut_term_ts` are wrong and no such executable is
> installed."* `command -v pnut-term-ts` finds nothing under that spelling either; the installed
> binary is `/usr/local/bin/pnut-ts`. Corrected to `pnut-term-ts` in the same pass — leaving it would
> have fixed half a sentence.
>
> **Every site was checked for sense, not just substituted** — this finding requires it ("check each
> site is the *command*"). Counted off the pre-edit backups: **23 of the 27 are inside backticks**
> (13 as `` `pnut_ts -d` ``, 10 as bare `` `pnut_ts` ``), unambiguously the command. The **other 4**
> are the compound adjective *"pnut_ts-verified"* — `architect-guide/CHANGELOG.md:102` and `:114`,
> `architect-guide-body.md:19`, `getting-started-body.md:17`. Those are the one shape where this
> finding says **PNut-TS** might be proper instead; they were still taken to `pnut-ts` because
> "verified by running it" names the *binary*, and that is the form already shipping in running text
> at `p2-assembly-language-manual/opus-master/CHANGELOG.md:196` ("348 code examples audited with
> pnut-ts v1.51.7"). Two of the four (`architect-guide-body.md:19`,
> `getting-started-body.md:17`) sit inside the masters' `<!-- CONVENTIONS -->` authoring comments and
> reach no reader — corrected anyway, because a convention block that names a non-existent binary is
> how the next author reintroduces it. The result matches the form P2AN001/P2AN002 already ship
> (`P2AN001/opus-master/P2AN001.md:622`, `P2AN002/opus-master/P2AN002.md:357`), so the set no longer
> teaches both spellings. `grep -c pnut_ts` over `manuals/*/opus-master/` + `app-notes/*/opus-master/`
> is now **0** outside `archived-2025/`.
>
> **Deliberately NOT swept, and why:** the 3 sites in
> `p2-pasm-desilva-style/opus-master/archived-2025/README-COMBINED-MASTER.md` — archived scaffolding
> that ships to nobody, excluded by this finding's own table. Frozen records under `audit/`,
> `archive/` and `code-validation/`, and the real path `external-inputs/pnut_ts_facts/`, are likewise
> untouched.
>
> **Gates:** `audit-code-line-length.py --budget 76` and `audit-inline-code-ascii.py` exit 0 on all
> 14 files. **No occurrence was inside a code fence** — verified by mapping every changed line number
> against the files' fence ranges — so no example file changed, byte-identity is untouched, and
> `pnut-ts` compilation does not apply to this finding.
>
> **What remains is publication, not authorship.** Nine reader-facing documents now carry the
> correction in source and none of them has been re-released: Getting Started, Architect's Guide,
> PNut-Term-TS Guide, and P2AN003–P2AN007. Each ships it at its next release. **This is not a render
> gate** — a token substitution has no layout consequence — so «#302» need not look at it; it is a
> release-wave item.

## Published PDFs carry no machine-readable rights (2026-08-21) — F-316

### F-316 — every published PDF states CC BY-SA 4.0 and a joint copyright on its own page, and carries neither in its metadata. `PARTIAL — mechanism DONE and PROVEN 2026-08-22; adoption is per document`

**How it surfaced.** Stephen, reading the Streamer v1.1.0 metadata at the «#287» gate, asked whether
the PDF's rights should name both companies. The `Author` field is correct as written — Iron Sheep
Productions is the author, and authorship is not copyright — but the question exposed that the
copyright and licence are **absent from the metadata entirely**.

**Measured on the returned v1.1.0 PDF:**

```
Title:            P2 Streamer Programming Guide
Subject:          Comprehensive Reference for Propeller 2 Streamer Hardware
Author:           Iron Sheep Productions, LLC
Custom Metadata:  no
Metadata Stream:  no          <- no XMP at all
```

while `front-matter.md:112` reads *"Copyright © 2026 Iron Sheep Productions, LLC and Parallax Inc."*
and the page below it grants **CC BY-SA 4.0**. Nothing in
`platform/templates/p2kb-platform-foundation.sty` sets `pdfkeywords`, and `hyperxmp` is not loaded,
so no `dc:rights` is emitted.

**Why it matters more than its size suggests.** CC BY-SA exists to be machine-readable. An
aggregator, a search index or a model crawler reading these files sees a document with no licence —
so a deliberately-open set reads as unlicensed, which is the opposite of the intent.

**The split is real, and the fix must respect it.** Surveyed 2026-08-21 across every manuscript:

| Population | Count | Copyright line |
|---|---|---|
| Manuals, guides and all 7 app notes | 17 | Iron Sheep Productions, LLC **and Parallax Inc.** |
| `pnut-term-ts-user-guide` | 1 | Iron Sheep Productions, LLC **only** |
| `Donna-Manuscript` | 1 | private, separate author — out of scope |
| `p2-layout-torture-test` | 1 | instrument, no copyright page — out of scope |

So the string **must be single-sourced per document from `request.json`**, never hardcoded in the
platform. A platform constant would silently attribute Parallax to the one document they have no
part in — precisely the class of defect the metadata single-sourcing work («#283») was built to end.

**Proposed correction.** Two new `request.json` metadata keys (`copyright`, `license`), consumed the
way `\DocTitle` / `\DocAuthor` already are. Emit through `\hypersetup{pdfkeywords=…}`, which needs no
new package; add XMP `dc:rights` via `hyperxmp` **only if** the Forge's TeX Live carries it — that is
unverifiable from the container and must be probed on the interactive daemon rather than discovered
in a production build.

**Sequencing — IN THIS WAVE. Stephen's call, 2026-08-21, overriding a first recommendation to
defer it.** The initial reasoning was that a platform change invalidates the built Streamer PDF and
everything queued behind it. That is true and it is the wrong trade: **this wave is the metadata wave
by design** — «#283» converted identity strings to platform single-sourcing and this release is the
first time the full metadata set reaches the documents. Deferring rights to a later adoption round
means a SECOND metadata round-trip for every document, and an interval in which every published PDF
carries half its metadata. One round-trip, complete, is cheaper and correct. Get it right the first
time it ships.

**Not a manuscript defect.** Every copyright page is already correct and states both parties where
both apply. Nothing in any master needs editing.

**Status:** `PARTIAL — the mechanism is DONE and PROVEN on a returned PDF; the other 17 documents adopt at their next render.`

> **PROVEN 2026-08-22 on the returned Streamer v1.1.0 PDF — read from the artifact, not the log.**
> `Keywords` now reads *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
> under CC BY-SA 4.0"*. `\DocCopyright`/`\DocLicense` join the `\Doc*` family, fed per document
> from its own `request.json`.
>
> **The build is byte-stable**: 91 pages, 24,737 words, and **ZERO pages whose text differs**
> from the pre-rights build — which is what a guarded metadata-only platform change should
> produce, and is now measured rather than assumed.
>
> **Two defects were caught by arming the gate against the returned build**, both mine, and both
> would have shipped: the first emitted string read *"Parallax Inc.. Licensed under"* because the
> template appended a full stop to a value that already ended in one (now a semicolon, fixed in
> the platform so none of the 17 documents still to adopt inherits it); and the gate itself was
> checking only that SOMETHING rights-shaped was present, never that the declared values actually
> arrived. It now verifies each one round-tripped. That is the second time in one day this gate
> passed on intent rather than artifact — worth remembering as a shape, not an incident.
>
> **Owed:** the other 17 documents, tracked in `PLATFORM-FEATURE-ADOPTION.md`'s new Rights column;
> and XMP `dc:rights`, which needs `hyperxmp` and stays gated on confirming that package exists in
> the Forge's TeX Live rather than assuming it. `Keywords` is the carrier today.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302»).** `pdfinfo` over all 15 files in
> `deliverables/documents/DOCs/`: **2 carry a rights `Keywords` string, 13 carry none.**
>
> - **Assembly Reference** — *"Copyright 2025-2026 Iron Sheep Productions, LLC and Parallax Inc.;
>   licensed under CC BY-SA 4.0"*
> - **Streamer Guide** — *"Copyright 2026 Iron Sheep Productions, LLC and Parallax Inc.; licensed
>   under CC BY-SA 4.0"*
> - **EMPTY:** Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide ·
>   XBYTE · P2AN001…P2AN007
>
> Both adopted strings use the **semicolon** form, so the *"Parallax Inc.. Licensed under"*
> double-stop defect is confirmed absent from everything that has shipped — the platform fix held,
> and none of the 13 still to adopt can inherit it.
>
> **The `pnut-term-ts-user-guide` split is intact and is the reason this must never become a
> platform constant:** its row is ✅ in the adoption table with the ISP-only string, distinct from
> the 17 joint-copyright documents.
>
> **Two things remain owed, and NEITHER can be discharged in this container:**
> 1. **13 published documents adopt at their next render** on `EXEC_ENV_CANONICAL`.
> 2. **XMP `dc:rights` stays gated on whether `hyperxmp` exists in the Forge's TeX Live** — a probe
>    on the interactive daemon, Stephen's side. Until then `Keywords` is the carrier and
>    `Metadata Stream: no` is expected, not a defect. **Do not "fix" this by loading `hyperxmp`
>    speculatively in a production build.**

---

## Nine documents carry a request.json subtitle their own cover contradicts (2026-08-22) — F-317

### F-317 — the subtitle in `request.json` disagrees with the printed cover in 9 of 15 published documents, and adopting metadata single-sourcing is what makes that visible. `PARTIAL` (re-verified 2026-10-05 «#386»: deSilva and Debug Window now agree; seven app-note subtitles still contradict their covers) — **all 9 re-measured 2026-08-25 («#302»): unchanged, still drifting, none adopted**

**How it surfaced.** Stephen: *"fix README if needed, always."* Sweeping the public index's
subtitle lines against the PDFs found 10 apparent mismatches — but checking them against
`request.json` was the wrong comparison, because **`request.json` only reaches the PDF for a
document that has ADOPTED metadata single-sourcing**, and only three have. Re-run against the
**printed cover**, the picture inverted: the README was right in almost every case, and it is
`request.json` that is out of step.

**The real defect, and it is latent rather than shipped.** For an unadopted document
`request.json`'s subtitle reaches nothing, so the disagreement is invisible. The moment that
document adopts — `\DocSubtitle` → `pdfsubject` — that string **becomes the PDF's Subject** and
contradicts the subtitle printed on its own cover. **This already happened once**: «#283» hit it
on the Streamer Guide, and the rule recorded then is **the cover wins**.

| Document | `request.json` subtitle | printed cover says |
|---|---|---|
| `p2-pasm-desilva-style` | Build, Experiment, and Master the Propeller 2 | A Human-Centered Approach to Parallel Processing |
| `p2-debug-window-manual` | See What Your Program Is Doing — Nine Display Windows for the Propeller 2 | See What Your Program Is Doing |
| P2AN001 | Application Note P2AN001 — No External ADC | Measure an Absolute Voltage in Microvolts on a P2 Pin |
| P2AN002 | Application Note P2AN002 — Hardware Math on the P2 | CORDIC for Real Work |
| P2AN003 | Application Note P2AN003 — No External DAC | Generate Analog Waveforms and Audio on a P2 Pin |
| P2AN004 | Application Note P2AN004 — No External Counter or ADC | Read Real-World Sensors by Frequency, Rotation, and RC Timing on a P2 Pin |
| P2AN005 | Application Note P2AN005 — Run Several Jobs in One Cog | Cooperative Multitasking with Spin2 TASK Methods |
| P2AN006 | Application Note P2AN006 — Size Every Stack, Catch Every Overflow | Sizing Cog & Task Stacks |
| P2AN007 | Application Note P2AN007 — STRUCT Records, Shared Safely Across Cogs | Data Structures with the New Language Facilities |

**Correction.** Before each document adopts metadata single-sourcing, bring its `request.json`
subtitle to the string its cover prints — **the cover wins**, per «#283». Doing it at adoption
time is the natural moment: that is the render where the value first matters, and
`audit-pdf-metadata.py` will compare the Subject against `request.json` on the returned PDF, so a
wrong value fails the gate rather than shipping. For the seven app notes, note their cover puts a
*descriptive line* under the title — decide per document whether that line or the catalog tagline
is the subtitle, rather than sweeping one reading across all seven.

**Also fixed here (2026-08-22):** the public index's bold line for the Streamer Guide read *"A
Guide to the Propeller 2 Streamer, Its Modes and Function"* while the document it links to prints
*"Comprehensive Reference for Propeller 2 Streamer Hardware"*. That one WAS shipped drift — the
catalog misdescribing the download — and is corrected. Every other index line was verified against
its cover and is correct; the app notes deliberately use `Application Note P2ANxxx · <topic>` as an
index label while their **heading** carries the cover's title, which is a consistent scheme, not
drift.

> **RE-MEASURED 2026-08-25 («#302») — all nine `request.json` subtitles read off disk: every one is
> UNCHANGED from the table above. The drift is intact, and none of the nine has adopted.** So the
> defect is still latent rather than shipped, exactly as recorded — but see the sharpening below,
> which changes when it stops being latent.
>
> ⚠️ **`pdfsubject` IS wired, so "latent until adoption" now means "fires at the very next
> adoption".** This entry was written while F-300 step 4 said *"Do NOT wire `pdfsubject`"*. The two
> adopted PDFs measured today both carry a populated `Subject` (Assembly: *"Complete PASM2
> Instruction Set Documentation"*; Streamer: *"Comprehensive Reference for Propeller 2 Streamer
> Hardware"* — the **cover** string, i.e. «#283»'s cover-wins rule already applied). Neither is in
> the drift table, which is why nothing has shipped wrong yet. **That is luck of ordering, not a
> guard.** The next of the nine to render will publish its `request.json` subtitle as the PDF
> Subject and contradict its own cover.
>
> **So the correction is now a PRE-RENDER step, not a same-render one:** bring the `request.json`
> subtitle to the cover string **before** staging that document, and let `audit-pdf-metadata.py`
> confirm it on the returned PDF. The seven app-note rows still need the per-document decision this
> entry calls for (cover descriptive line vs catalog tagline) — **do not sweep one reading across
> all seven.**

**Status:** `PARTIAL — resolve each document's subtitle to its printed cover BEFORE the render that adopts metadata single-sourcing; 2 of 9 resolved (deSilva, Debug Window), the seven app notes still drifting (re-verified 2026-10-05 «#386»).`

## Open — enhancement proposals (new content, not corrections)

- **ENH-03 — a gating compile step for every code block in `deliverables/ai/P2/`.**
  > **DECIDED by Stephen 2026-10-08: build it now, as the first item of the close-out. From here
  > on it is a permanent part of the release gate** ("let's get this built and from here forward be
  > part of our actual gate!"). It is a hard gate in `release-yamls` and an edit-time check in
  > `yaml-knowledge-base-maintenance` on the files touched. Order: (1) the per-block markers
  > (`compile: program` / `fragment` / `never` + reason, with `never` asserted to fail); (2) fix
  > the prototype's auto-declare collision ("Symbol is already defined") before trusting any pass
  > rate; (3) wire the gate into both skills; (4) all close-out corrections are made under it.
  > F-381's "the example is correct" depends on it.

  > **PROGRESS 2026-10-08 — B1+B2 built («#400»); B3 classification «#403» and B4 wiring «#404»
  > open.** Design: `engineering/analysis/2026-10-08-enh-03-compile-gate-design.md` (approved).
  > Gate: `engineering/tools/validation/audit-kb-code-compiles.py`; manifest root
  > `engineering/tools/validation/kb-compile-manifest/` (sidecars, never shipped). Points (1) and (2)
  > above are delivered: classes live in the sidecar manifest, not in the YAML, and the proposer
  > attributes each collision to the one name that caused it. `--negative-control`: 17 controls
  > (the 11 designed plus 6 opposite-case companions) all hold, and each fires when its guard is
  > removed (arbiter re-run: PASS, 2.1 s). **Re-measured census** (supersedes the 1913/438 figure
  > above): 1130 files, 0 parse errors; **2963 candidates in 581 files** (2476 under a code-named
  > key, 897 of those single-line; 487 found by compiler-recognised shape only); 2066 multi-line
  > in 498 files, 155 with `debug(`. Proposer over all 2963: 438 program, 1687 fragment,
  > **836 FAIL (B3's triage input)**, 2 HARNESS. Speed (24 cores): a populated full sweep 26 s; the
  > proposer 2 m 13 s — the "~25 min" estimate above does not hold. PNut-TS hang on a file with no
  > final newline is worked around (the gate adds one) and filed as punch-list item 5.

  > **PROGRESS 2026-10-09 — B4 done («#404»): the gate is a permanent release gate.**
  > `validate-dod-release.py` runs `validate_kb_code_compiles()` (negative control, then the full
  > sweep with its own 900 s timeout — measured 27 s wall / ~520 s CPU on 24 cores; the inherited
  > 300 s would not cover a single-core machine). `audit-gate-arming.py --show-tiers` lists it
  > ARMED by the runner. `release-yamls` names it as a BLOCKING §1 precondition, a §1.5 standing
  > check (`--since "$PREV"` plus an audit of the manifest diff — moves into `never`/`not-code`,
  > new `assumes` names and deleted entries are the hunks auditors read), in §5.5's command list
  > and in *What a green gate does NOT certify*. `yaml-knowledge-base-maintenance` gained §2.6
  > *Compile the code you touched* and a hand-back line. A DoD run now includes it and is RED on
  > the 352 registered blocks: no release until the close-out fixes them, as decided. Full sweep
  > time on Stephen's machine is not yet measured. The ENH-03 build is complete; this entry closes
  > when the close-out release ships green.

  > **PROGRESS 2026-10-09 — B3 done («#403»).** Every candidate is
  > classified: **3077 blocks — 501 program, 1932 fragment, 17 never (asserted to fail), 627
  > not-code (each with its reason)**, in sidecars under `kb-compile-manifest/`. A full sweep takes
  > 27 s and fails on **352 blocks, every one REGISTERED** against a close-out study row (105
  > distinct rows) — none unclassified, none unregistered, no tooling gap left. Ten review groups,
  > each a fresh reviewer, verified by the arbiter in a fresh scratch root before writing the real
  > manifest; evidence in `engineering/analysis/2026-10-08-p2kb-close-out-evidence/`. The review
  > also produced **266 study rows** (S-001..S-266) — compile defects and the prose defects the
  > reviewers read on the way — in `engineering/analysis/2026-10-08-p2kb-close-out-study.md` §3.
  > Five tooling passes widened the harness honestly (version-gated built-ins, flow statements in
  > the net, result/VAR wraps, valued constants, STRUCT types, PASM labels, end-of-file `never`);
  > 37 negative controls, each shown to fire when its guard is removed. The census grew 2963 →
  > 3077 when the net learned flow statements (S-109). Two compiler questions went to the PNut-TS
  > punch list (items 6, 7), each to be checked against PNut first. Still outside the net by design:
  > single-line strings (S-256 asks whether tutorial one-liners should come in) and text YAML has
  > already cut (S-183/S-200: 47 served strings truncated at ` #`; needs its own gate).

  > **Drained for `language/pasm2` 2026-10-10 («#418»).** Every pasm2 finding in the manifest is
  > gone (86 entries in 29 files → 0 `finding:` under `kb-compile-manifest/language/pasm2`; the
  > 18 `S-137` quick_example entries were already compiling). The ` #` plain-scalar gate
  > (`audit-yaml-plain-scalar-comment.py`) reads 47 flagged in 15 files → 0; the D3 bare-constant
  > sites (`false`/`true`/`negx`/`posx`/`multi_cog_synchronization`) → 0. Stack: EF-094 — a 9th
  > push discards the oldest entry and entries are 32 bits (the "22 bits" claim is gone from
  > `stack_operations.yaml` and `architecture/cog.yaml`, whose push/pop lists also named CALLA/CALLB/
  > CALLD/RETA/RETB, which use no hardware stack); EF-101 — a zero XORO32 state is absorbing.
  > Wider findings fixed in the same pass: the ALTS+`JMP #0-0` computed-jump idiom (the immediate
  > branch assembles as a relative offset, so the substituted S field gives a wrong target) is now a
  > table of `JMP #case` entries entered with `JMP reg`; `architecture/cordic.yaml` `pollqmt` was
  > "check if CORDIC pipeline empty" (the QMT flag is set by a GETQX/GETQY with nothing queued);
  > the WAIT-family `timing.cycles: 2` is now `2+` as each page's encoding says (15 pages); the
  > Spin2 `spin2-pasm2-integration` `JMP @slowCode` register-indirect form is `JMP #\@slowCode`.

  *Filed 2026-08-21;
  Stephen's call, and he asked for it in these words: "we must, for all code in YAML files, compile
  that code and assure ourselves that it compiles correctly. We do not publish a release unless all
  the code publishes correctly."* Nothing in this project compiles KB code examples, which is how
  F-311…F-313 and F-315 shipped. **Census: 1913 code-shaped blocks across 438 files; only 118 are
  complete programs, so 1795 need a synthesized context.** Design points already settled:
  - **The blocker is not the compiler, it is that the KB never declares which strings are code.** A
    heuristic sweep pulled 166 of 541 PASM2-shaped blocks out of *prose* fields. So the first
    deliverable is a per-block marker — `compile: program` / `compile: fragment` /
    `compile: never` + reason — not a runner. A guessing gate cries wolf, and a gate that cries wolf
    gets ignored.
  - **`compile: never` must be ASSERTED TO FAIL**, not skipped. The KB teaches anti-patterns; a
    wrong-code example that quietly starts compiling means the wrongness was edited away.
  - **It proves LEGALITY, not correctness**, and must never be cited otherwise. F-312 is the proof:
    fixing `qvector y_val` so it assembles would have left X and Y still swapped.
  - **No build stamps** (PL-004). The gate runs against whatever compiler is installed; a bump that
    breaks something turns the release red, which is the gate working. That is also what makes the
    surviving `re-verify on a compiler version bump` notes deletable.
  - Prototype validated 2026-08-21: it asks the compiler which identifiers are declarable rather than
    carrying a keyword list that would rot. 4/4 known-bad caught, 4/4 known-good passed. Its known
    weakness is auto-declaration colliding with symbols a block defines itself, which produced
    `Symbol is already defined` on blocks that compile correctly by hand — fix that before trusting
    any pass-rate number from it.
  - Hooks: `release-yamls` as a hard gate (~0.8 s/block, ~25 min full sweep), and
    `yaml-knowledge-base-maintenance` on touched files so it fails at edit time, not release time.

- **ENH-02 — make the platform fail loudly on a code line that cannot fit.** *Filed 2026-08-21 when F-281 closed.* F-281's three over-wide lines were fixed and v1.1.3 shipped margin-clean, but **nothing stops the class recurring**: `p2kb-platform-code-coloring.lua` emits `\begin{Verbatim}[xleftmargin=-10pt]` with no break options at all ten sites, and the `breaklines=true` at `p2kb-platform-foundation.sty:317` is a pre-existing `\lstset` that the Verbatim path never consults. So an over-long line silently runs off the page and the compile log stays clean — the exact shape of every render defect this project has shipped. The source-side `audit-code-line-length.py` gate catches most of it, and `audit-pdf-margin-overflow.py` catches it after the fact; what is missing is the platform refusing to typeset it. Not a defect in any document — an absent guard.

- **ENH-01 — Harvest the Architect's Guide *project front-end* into a new KB node set.** *Scheduled
  2026-07-08 (deferred from the Architect's Guide v1.0.0 release); Stephen go/no-go before authoring.*
  Source: *The P2 Architect's Guide* v1.0.0, **Part I (Act I)**. The decomposition-reasoning layer
  (`architecture/decomposition/`) begins *at* "which cog owns what"; nothing in the KB captures the
  **pre-decomposition** front-of-project work Part I lays out. Candidate new node set — reusable P2
  **design-process** patterns that sit *above* the decomposition layer: feasibility-before-design ·
  **narrow-vs-broad comms selection** (I²C/SPI vs host-style ribbon) · **offload-vs-port /
  companion-device partitioning** · pin-budget → adapter-board · "characterization becomes the spec" ·
  firmware-loaded-device → loader. Also a small KB touch worth doing: **performance → P2-resource
  mapping** (which performance need → LUT RAM / PSRAM / CORDIC / streamer — Architect's Guide Act III
  P-7). **Do NOT harvest the Act III agentic principles** (about *using agents*, not the P2 — low KB
  value). Fuller rationale table lives in the manual's `PLANNING.md` (KB-harvest proposals).

---

## Open — TRACKED in the ingestion head (resolution lives there, not in a YAML edit)

- **F-123 — TAQOZ-Forth / ROM-Monitor capability detail rests partly on preliminary web research.** `TRACKED → ingestion` Grounding plan in `engineering/ingestion/sources/taqoz/taqoz-content-gaps-and-grounding-plan.md` (mine `ROM_Booter.lst`; verify vs Peter Jakacki's `TAQOZ.spin2`).
  > **Routing re-verified 2026-08-25 («#300») — still live, and one of its two inputs is missing.** The
  > routing target resolves: the grounding plan exists at the path above, and the first input is in hand —
  > `engineering/ingestion/sources/rom-booter/ROM_Booter.lst` **and** `rom_booter_v33_01j.lst` are both
  > present (the `v33_01j` copy is the one E-005 cites, so it is the mined edition). **The second input is
  > NOT in hand:** no `TAQOZ*.spin2` exists anywhere in the repo, so the *"verify vs Peter Jakacki's
  > `TAQOZ.spin2`"* half cannot run today. **What would settle it:** obtain Jakacki's `TAQOZ.spin2` source;
  > until then the ROM-monitor half is groundable from `ROM_Booter.lst` alone and the Forth-vocabulary half
  > is not. Stays `TRACKED → ingestion` — the preliminary web-research material
  > (`taqoz-web-research-preliminary.md`) remains community-tier and is still not citable.
  >
  > 🔴 **CORRECTED 2026-09-10 by F-421 — this plan names the WRONG listing.** *"mine
  > `ROM_Booter.lst`"* points at the **FPGA** build (`ver = "A"`, Prop123-A9/BeMicro-A9).
  > The chip's ROM is `rom_booter_v33_01j.lst` (`ver = "G"`, Prop2 Silicon v2) — same source
  > version v141, different build target. Mine THAT one; the FPGA listing carries FPGA clock
  > constants, a different SD call structure, and a reserved long that silicon uses for MBR
  > validation. Keep `ROM_Booter.lst` only as the labelled FPGA comparison point.

---

## Render-verification wave — defects found by READING the generated PDFs (2026-08-17/19) — F-284…F-294, F-299…F-301

**Origin.** Verifying the six generated wave PDFs page by page rather than reading their compile
logs. Every finding below was invisible to a clean log: LaTeX ate an operator, a filter split a
line, a glyph printed nothing, a gate skipped the blocks it was built to check. F-295…F-298 closed
at the XBYTE sprint closeout and are archived.

> **These sat under the wrong header until 2026-08-21.** The 2026-08-19 sweep archived
> F-259…F-263 but left their `## Community bench review — refaQtor` header in place, so all
> fourteen read as part of a third party's bench review. That header is now in the archive with
> the findings it introduced. Detected by `audit-register-hygiene.py` check 9.

### F-301 — the cross-ref filter's adopt-at-next-release rule was passed over about a dozen times, because nothing read the tracker. `PARTIAL` (re-verified 2026-10-05 «#386»: the structural fix landed; only P2AN003, P2AN005 and P2AN006 still lack the cross-ref filter) — **detected 2026-08-19 by comparing the tracker against every `request.json`**

**The rule, written into `CROSSREF-FILTER-ADOPTION.md` when the filter shipped 2026-06-26:**
*"The next time each manual is released (for any reason), its release MUST add
`p2kb-platform-crossref` to that manual's `request.json` `lua_filters` and visually audit the
rendered PDF."* The tracker even names its own consumer — *"`release-manual` Phase 1/Phase 4
**should** consult this tracker."*

**Measured, not assumed.** Every workspace `request.json` read directly against the tracker's rows:

| Document | Tracker | In `request.json`? | Releases since the rule |
|---|---|---|---|
| Assembly | ⏳ pending, at v3.1.0 | **no** | v3.1.1 → v3.1.6 |
| DeSilva | ⏳ pending, at v3.0.1 | **no** | v3.0.2 → v3.0.6 |
| Debug Window | ⏳ pending, at v1.0.1 | **no** | v1.0.2 → v1.1.3 |
| Getting Started | ⏳ pending, at v1.0.0 | **no** | v1.0.1 → v1.0.3 |
| Architect | ⏳ "in development" | **no** | released v1.0.3 |
| XBYTE | **absent from the table** | **no** | v1.0.0, v1.1.0 |
| 7 app notes | **absent from the table** | **no** | 20+ |
| IOSP | 🔧 adopting (pilot) | yes, ordering correct | audit never recorded |
| Streamer | ✅ adopted + audited | yes, ordering correct | — |

**Only two of fifteen ever adopted.** IOSP's row still reads "awaiting Stephen's regen + visual
audit" although it has released three times since, so its filter has certainly rendered — the
**audit** is what is unrecorded, and that half is the half that matters (a mis-fired auto-link is
exactly what the audit exists to catch).

**The statuses are not wrong. Nothing read them.** Every row above is an accurate record of a
decision that was then never consulted at the moment a release happened. This is the same failure
as [[F-281]]'s «#250» in a different costume — a correct record that is not where the decision gets
made — and it is why adoption state moved into `PLATFORM-FEATURE-ADOPTION.md`, which
`prepare-manual` consults on every prepare rather than "should" consult on release.

**FIX — structural, landed 2026-08-19:** one per-document × per-feature matrix
(`PLATFORM-FEATURE-ADOPTION.md`), seeded from **detected** state rather than from what each tracker
claimed, plus a `prepare-manual` check that surfaces a document's outstanding ⏳ features as work
owed **this** release. `CROSSREF-FILTER-ADOPTION.md` keeps the mechanism (including the mandatory
crossref-before-tables ordering) and its status table is frozen as history.

**Still owed per document:** the adopt + visual audit itself, at each document's next release —
that has not been shortcut, only made visible. **ssdb and pnut-term-ts release next and both sit at
⏳**, so they are the first two chances to stop the count growing.

> **RE-MEASURED 2026-08-25 («#302») — read out of every workspace `request.json`, not off the
> tracker, and the two agree row for row.** `p2kb-platform-crossref` present in the `lua_filters`
> list:
>
> | | Documents |
> |---|---|
> | **ADOPTED (4)** | Assembly Reference · I/O & Smart Pins · Streamer Guide · **PNut-Term-TS User Guide** |
> | **⏳ still owed (11 P2 documents)** | Architect's Guide · Debug Window · Getting Started · DeSilva · XBYTE · Single-Step Debugger · P2AN001…P2AN007 |
> | out of scope | `ai-privacy-guide`, `Donna-Manuscript` (private, non-P2), `p2-layout-torture-test` (instrument) |
>
> **The count stopped growing, which is the first evidence the structural fix works.**
> `pnut-term-ts-user-guide` was one of the two "first chances" this entry named, and it **took**
> the feature — adopted **and audited 27 of 27 on the returned PDF** (2026-08-23), the audit half
> that IOSP's pilot row never recorded. The other named chance, **Single-Step Debugger, is still
> ⏳** and is the next test of it.
>
> **This stays `CONFIRMED` because the per-document work is genuinely outstanding, not because
> anything is unknown.** Two things ride every future adoption and must not be dropped:
> **`p2kb-platform-crossref` MUST sit between `figures` and `tables`** (`tables` flattens each cell
> to a string and would leave table-borne refs dead — verified ordering in all four adopted
> `request.json`s), and **the visual audit on the returned PDF is the half that matters**, because
> a mis-fired auto-link is exactly what it exists to catch.

### F-300 — every published PDF in the set ships with empty Title and Author properties. `PARTIAL` — **MECHANISM LANDED + PROVEN 2026-08-19; 10 of the 17 published PDFs have adopted, 7 owed at their next render (re-measured 2026-09-21, «#344»)**

> **RE-MEASURED ON THE RELEASED ARTIFACTS 2026-09-21** («#344») — `pdfinfo` over every PDF in
> `deliverables/documents/DOCs/`, read from the shipped files themselves, not from a render log and
> not from this register. **10 of 17 now carry both Title and Author** (all `Iron Sheep Productions,
> LLC`), against 2 of 15 at the 2026-08-25 measurement. The set grew by two documents in the
> interval, so the denominator moved as well as the numerator.
>
> **Still empty, and each resolves at that document's next render — this is the expected shape of
> this finding, not debt:** `P2AN003` · `P2AN005` · `P2AN006` · `P2AN007` ·
> `P2-Architect-Guide` · `P2-Debug-Window-Manual` · `P2-XBYTE-Programming-Guide`.
>
> Status stays open deliberately: it is manual-head and per-document, so it cannot close until the
> last of those seven re-renders. It is `PARTIAL` rather than `PENDING-VALIDATION` because the
> mechanism is proven and adopting is now routine — what remains is render scheduling, not
> validation.

> **ADOPTION MEASURED ON THE ARTIFACTS, 2026-08-25 («#302») — `pdfinfo` over every file in
> `deliverables/documents/DOCs/`, not read off the tracker.**
>
> | State | Count | Which |
> |---|---|---|
> | **Title + Author + Subject + Keywords populated** | **2** | Assembly Reference (`P2 Assembly Language Reference Manual` / `Iron Sheep Productions, LLC`), Streamer Guide (`P2 Streamer Programming Guide` / same) |
> | **all four fields still EMPTY** | **13** | Getting Started · I/O & Smart Pins · DeSilva · Debug Window · Architect's Guide · XBYTE · P2AN001…P2AN007 |
>
> The mechanism is also proven on two documents that are **not yet published to `DOCs/`**
> (Single-Step Debugger, PNut-Term-TS User Guide), so four conversions exist in total.
>
> **This stays `PENDING-VALIDATION`, and it closes per document, on a render — never on an edit
> here.** Each of the 13 adopts by rendering on `EXEC_ENV_CANONICAL`; there is no container-side
> action that can advance it. Per-document state is `PLATFORM-FEATURE-ADOPTION.md`, which
> `prepare-manual` consults, and the measurement above agrees with it row for row.
>
> ⚠️ **`pdfsubject` IS being populated**, contrary to this entry's step 4 (*"Do NOT wire
> `pdfsubject`"*): both adopted PDFs carry a `Subject`. That does not misreport either of them —
> neither appears in **F-317**'s drift table — but it means F-317 is **live at every adoption**, not
> deferred, and each of the 13 must have its `request.json` subtitle reconciled to its printed cover
> **before** it renders.

> **RESOLUTION (2026-08-19).** The fix is **not** the one-line `pdfusetitle` this entry proposed —
> that would have populated the info dictionary and left the cover as a second hand-maintained copy
> of the same five strings, and would have shipped *wrong* titles on 9 of 15 (see the template table
> below). What landed instead: **every identity string lives once, in the document's `request.json`
> metadata, and reaches both the PDF info dictionary and the cover page from there**, via
> `\DocTitle`/`\DocSubtitle`/`\DocVersion`/`\DocDate`/`\DocAuthor` defined in
> `p2kb-platform-foundation.sty` (§ DOCUMENT METADATA). The macros carry the *value*; the cover keeps
> its *presentation*.
>
> **Proven on the interactive daemon, four round-trips, by reading the rendered PDF** — not the
> success flag. Both first converts (Single-Step Debugger, PNut-Term-TS User Guide) came back with
> compile logs clean on every serious signature and Title/Author/Subject populated for the first
> time, covers rendered and looked at. Commit `09958b0a`.
>
> **Unconverted documents are safe:** the foundation `\providecommand`s all five macros empty, so a
> template that has not opted in writes exactly what it wrote before. **Per-document adoption state
> is `PLATFORM-FEATURE-ADOPTION.md`**, and `prepare-manual` now reads it. The analysis below stands
> as the record of how the fix was found; only the proposed one-liner is superseded.

**Surfaced by** the Streamer v1.0.9 release verification — reading the delivered PDF's metadata
dictionary, then checking whether it was a Streamer regression. It is not: **all 15 PDFs in
`deliverables/documents/DOCs/` report `(empty)` for both `title` and `author`** — eight manuals and
seven app notes. Only `creator` (`LaTeX with hyperref`) and `producer` (`xdvipdfmx`) are set.

**What a reader sees.** A PDF viewer's title bar and Document Properties fall back to the *filename*
instead of the document's name, and anything indexing the file — a search tool, a library, a
citation manager — finds no title or author to key on.

**The mechanism, traced end to end.** The `.latex` template sets `\title{P2 Streamer Programming
Guide}` (generated `.tex` line 31), and `p2kb-platform-foundation.sty:259` sets a `\hypersetup`
block — but that block configures **only** link colors and bookmarks. It never sets `pdftitle` or
`pdfauthor`, and **hyperref does not derive them from `\title{}` on its own**; that requires either
`pdfusetitle` or explicit keys. So the title exists in the document body and never reaches the PDF
info dictionary.

**FIX (one line, in the shared platform):** add `pdfusetitle` — or explicit
`pdftitle={...}, pdfauthor={...}` — to the `\hypersetup` block at
`p2kb-platform-foundation.sty:259`. **Zero layout risk**: it writes the PDF info dictionary only and
cannot reflow a page. This is what distinguishes it from [[F-299]], which is parked because it
*does* move type.

**Corrects a claim in our own process doc.** The `prepare-manual` skill states that a `request.json`
metadata change "feeds PDF properties, not just the build." For this manual-production path that is
**not true** — the template hardcodes `\title{}`, and nothing carries `request.json`'s
`metadata.{title,author,version}` into the PDF info dictionary. Re-staging `request.json` on a
document switch is still mandatory for a different and real reason (input/template/filters), so the
rule stands; only its stated justification about PDF properties is wrong. Fix that sentence when the
platform fix lands.

**Sequencing.** No manual should re-render just for this. Let it ride with the next render each
document takes anyway, and take it in the same set-wide sweep as [[F-299]] — one `forge-test` pass,
two set-wide render changes.

> **Stale reference removed 2026-08-19.** This sentence named the fancyvrb `breaklines` work «#250»
> as a third member of the sweep. That work was **REJECTED 2026-08-17** on the round-trip evidence
> (see [[F-281]]); the reference was written after the rejection and never checked against it. The
> sweep is F-300 + F-299, and F-299 is polish. There is no breaklines work to schedule.

⚠️ **TRAP FOR WHOEVER TAKES THIS FIX — the two title sources already disagree.** Because nothing
consumes `request.json`'s metadata today, nobody has had to keep it in step with the cover, and it
has drifted. On the Streamer: the **cover** reads *"Comprehensive Reference for Propeller 2 Streamer
Hardware"* while `request.json` reads *"Comprehensive Reference for the Propeller 2 Streamer"*. The
moment `pdftitle`/`pdfsubject` start being populated, whichever source the fix wires up becomes
reader-visible, and a stale one ships silently. **Before adopting: audit cover-vs-`request.json`
across all 15 documents and reconcile, then decide which source is authoritative** (the cover is
what a reader actually sees, so it should win). Do not wire the metadata through without that pass.

**THAT AUDIT IS NOW MEASURED (2026-08-19), and the drift is systemic, not a Streamer typo.** Comparing
each master's cover block (`\fontsize{36}…\bfseries` title + `{\Large\itshape …}` subtitle) against
its `request.json` `metadata.subtitle`, over the 15 published documents:

| Verdict | Count | Which |
|---|---|---|
| **SAME** | 3 | Architect, Assembly, Getting Started |
| **DRIFT** | 8 | Debug Window, Streamer, P2AN001, P2AN002, P2AN003, P2AN004, P2AN005, P2AN007 |
| **cover block not matched by this scan** | 4 | IOSP, deSilva, XBYTE, P2AN006 — a different cover shape, **unresolved, not clean** |

**Two of the drifts are kinds of drift, not typos, and they change what the fix has to decide:**
1. **The app notes disagree structurally.** `request.json` carries a *catalog label* — "Application
   Note P2AN001 — No External ADC" — while the cover carries a *reader subtitle*: "No external ADC —
   a single-pin instrumentation ADC…". Neither is a stale copy of the other. Wiring the cover through
   verbatim drops the P2AN00N designator from the PDF's Title; wiring `request.json` through gives
   every app note a title that is not what its cover says. **Decide this before touching the
   platform** — likely `pdftitle` = title + designator, `pdfsubject` = the reader subtitle.
2. **Cover strings contain LaTeX.** PNut-Term-TS's cover subtitle carries a literal `\\` line break.
   PDF info-dictionary fields are plain text, so any such markup must be stripped, not passed through
   — one more reason `pdfusetitle` (which takes `\title{}` as-is) is not automatically the right
   mechanism for the subtitle half.

Truncation was not checked: two of these subtitles run past 50 characters and the register scan
compared full strings, so the counts above are exact for equality but say nothing about length limits.

---

**⚠️ THE SUBTITLE DRIFT IS NOT THE GATE. The gate is the templates, and nobody had looked at them
(traced 2026-08-19).** `pdfusetitle` populates `pdftitle` from `\title{}` and `pdfauthor` from
`\author{}` — it never touches the subtitle. So the drift table above gates only a `pdfsubject` we do
not have to wire. What actually decides whether this fix can be turned on and left to ride is what
each template declares, and **9 of the 15 declare something wrong:**

| Template `\title{}` | Documents | Verdict |
|---|---|---|
| `P2 Application Note` (hardcoded, SHARED) | **all 7 app notes** | **BROKEN** — `pdfusetitle` gives seven distinct documents one identical title. Worse than empty in a library or index. |
| `P2 XBYTE Programming Guide` | XBYTE | **STALE** — the released v1.1.0 cover reads *"P2 Interpreters & Emulators Guide"*. The template kept the pre-retitle name. |
| *(no `\title` and no `\author` at all)* | deSilva | **EMPTY** — would stay broken after the fix. |
| correct, matches cover | Architect, Assembly, Debug Window, Getting Started, IOSP, Streamer | ready |

`\author{Iron Sheep Productions, LLC}` is correct in every live template **except deSilva's**, which
has none.

**The one fact that makes all of this safe: `\title{}` is never rendered.** Every cover in the set is
hand-built in the master's `front-matter.md` (`\fontsize{36}{42}\selectfont\bfseries …`). There is no
`\maketitle` anywhere in the published set — the only one in the tree is in `ai-privacy-guide`, which
is not a published document. **So `\title{}` is metadata-only, and changing it cannot move a single
point of type on any page.** That is what turns this from a render-risk change into a ride-along.

**REVISED PLAN — prep in one commit, no renders, then ride:**
1. **Switch every live template from a hardcoded `\title{…}` to `\title{$title$}` / `\author{$author$}`.**
   `request.json` becomes the single source and a template can never go stale against its document
   again — this is what fixes the seven app notes and XBYTE at once, and it is durable rather than a
   catalog of literals to maintain. Verified safe: **`request.json` `metadata.title` equals the cover
   title for 14 of 15**, including all seven app notes (the cover carries the designator on its own
   eyebrow line — *"Propeller 2 • Application Note P2AN006"* — above the title, so nothing is lost).
2. **deSilva is the one real conflict, and it is BOTH fields.** Released cover: *"P2 Assembly
   Programming"* / *"A Human-Centered Approach to Parallel Processing"*. `request.json`:
   *"Discovering P2 Assembly"* / *"Build, Experiment, and Master the Propeller 2"*. The cover wins →
   update `request.json`, then give `p2kb-desilva.latex` the same `$title$`/`$author$` pair.
3. **Add `pdfusetitle`** to the `\hypersetup` at `p2kb-platform-foundation.sty:259`.
4. **Do NOT wire `pdfsubject`.** Leaving it out defers the whole subtitle question above at zero cost;
   revisit it as its own item whenever someone wants Subject populated.
5. **Add a `PLATFORM` ledger line and let each document absorb it at its next natural render.**
   Precedent for the standing: the 2026-07-13 mnemonic-bold line — *live-but-benign, not outstanding
   debt*. No manual re-renders for this.

**One `forge-test` still confirms three things before adoption**, none of them layout: that `$title$`
substitution actually reaches `\title{}` on this path, that `&` survives into the info dictionary
(IOSP *"P2 I/O & Smart Pins User Guide"*, P2AN006 *"Sizing Cog & Task Stacks"*), and that `pdfauthor`
lands. Read the output PDF's metadata dictionary, not the compile log.

### F-299 — wide `tblr` tables overhang the right text edge by ~5–6pt, in the platform, not the manual. `CONFIRMED` — **POLISH, NOT A GATE FAILURE: it is inside the project's own 20pt tolerance (re-graded 2026-08-19, same day, see the correction at the end)**

**Surfaced by** the Streamer v1.0.9 daemon pre-verify — a whole-document margin measurement of the
rendered PDF (every text span's `x1` against the 540pt text edge), not by the compile log, which was
clean on every serious signature in both the v1 and v2 renders.

**The defect.** Two of the Streamer's wide mode-reference tables push their rightmost column past
the text block: §6.2 *RDFAST → Pins/DACs* by **6.1pt** (`DAC Bits` header) and §8.x *Pins/DACs →
Hub* by **5.3pt** (`Hub Write` header). Visible as the table's horizontal rules extending past the
running-header rule directly above them. The compile log reports these as `Overfull \hbox
(26.6406pt too wide)` — the larger number is the whole `tblr` box including padding; the visible
overhang is the 5–6pt the measurement above reports.

**Why it is the platform's, not the manual's.** The column widths are computed by
`p2kb-platform-tables.lua`, which every manual in the set loads. Nothing in the Streamer's markdown
sets a width. A manual-side "fix" would mean hand-tuning a table the filter is supposed to own.

**NOT the two tables an earlier note predicted.** The Streamer release note expected the
`p2kb-platform-tables.lua` column fix to absorb "2 over-wide `Constant | Value | Description`
tables". These two are **6-column** `Mode | Symbol | Type | Pins | DAC Channels | DAC Bits` tables —
a different shape the fix does not reach. The prediction was not wrong about its own targets; it
was applied to the wrong pair. **A status note naming a fix is not evidence the fix covers what you
are looking at** — measure the artifact ([[feedback_status_line_is_not_evidence]]).

**Deliberately not fixed in this release.** A column-width change in
`p2kb-platform-tables.lua` reflows tables in **every** manual, so adopting it while Streamer is
mid-render means re-verifying the whole set against a changed table model for 6pt of rule overhang.
Schedule it when no manual is mid-render, and expect the absorbing manual's next render to shift
table layout. **Pair it with [[F-300]]** — both are set-wide render changes whose failure mode is a
page that looks fine in the log, and both want one `forge-test` sweep across the set rather than two.

> **Stale reference removed 2026-08-19.** This paragraph cited the fancyvrb `breaklines` work «#250»
> as the precedent it followed and the partner to pair with. That work was **REJECTED 2026-08-17**
> ([[F-281]]) — before this entry was written. The scheduling rule it borrowed is sound and stands on
> its own; the partner is F-300.

**Scope when taken:** measure every manual, not just the Streamer — the filter is shared, so any
manual with a 6-column table is a candidate.

---

⚠️ **CORRECTION, same day, before this entry could mislead anyone — I RE-GRADED MY OWN FINDING.**

I measured this with a hand-rolled PyMuPDF scan at a **4pt** threshold. **The project already has a
sanctioned instrument for exactly this** — `engineering/tools/validation/audit-pdf-margin-overflow.py`
— and I did not use it. Run against the shipped v1.0.9 PDF it reports:

```
text-block right edge: prose 540.0pt, code 540.0pt   (tolerance 20pt)
CLEAN  nothing crosses the margin (76 pages measured)
```

**The gate's tolerance is 20pt by design. These tables are 6.1pt and 5.3pt — comfortably inside it.**
So both statements are true and the second is the one that sets priority: the overhang is real and
visible if you look for it (the table rule extends a hair past the running-header rule), and it is
**not** something the project's own margin gate would ever block on.

There is direct precedent for accepting far more: the IOSP v1.0.9 PUBLISH line accepts a chart
bleeding **~24pt** past the text block on evidence — zero overlapping spans measured, every cell
readable — with the explicit note that *magnitude is never the verdict*. A 6pt rule overhang with no
overlap is a smaller version of the same accepted case.

**Re-grade: this is POLISH, not a defect owed.** Still worth taking in the set-wide sweep with
[[F-300]] because the fix is cheap once the platform is open anyway — but it must not be
described as a defect blocking anything, and no manual should re-render for it.

**The transferable lesson — the one worth more than the finding.** Reach for the project's own
instrument before hand-rolling a measurement. Mine was not wrong, but it carried **no calibrated
threshold**, so it reported a number without the judgement that makes the number mean something, and
I very nearly filed a tolerance-conformant table as a defect owed. A raw measurement is not a
verdict; the tolerance IS the verdict ([[feedback_validation_tool_verdict_is_a_claim]] — the inverse
case, where the tool PASSES and the hand-rolled scan is the one overstating).

> ### DISPOSITION CONFIRMED 2026-08-25 («#300») — the re-grade stands; nothing re-measured, nothing re-argued
>
> Carried on «#300»'s roster and **closed here as POLISH, per the same-day correction above.** The 6.1pt and
> 5.3pt overhangs sit inside this project's **20pt** margin tolerance, so
> `audit-pdf-margin-overflow.py` — the sanctioned instrument — reports the shipped v1.0.9 PDF **CLEAN across
> all 76 pages**. **The tolerance IS the verdict.**
>
> **Deliberately NOT re-measured.** A disposition already made on evidence does not get re-litigated by a
> later agent hoping for a different number; re-running the hand-rolled 4pt scan would only reproduce the
> mistake the correction above documents. **No PDF was re-graded and no manual re-rendered for this.**
>
> **Not a gap and not a defect owed** — it is scheduled work with no blocker: take it in the set-wide
> `p2kb-platform-tables.lua` sweep, paired with **F-300**, when no manual is mid-render. Nothing in this
> sprint is waiting on it, and **no document may cite it as blocking**.
