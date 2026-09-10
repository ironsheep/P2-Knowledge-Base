# YAML shape change — consumer audit

**Answers:** `2026-08-25-yaml-release-change-ledger.md` §0.3 item 6 / §1.10, *"Shapes changed under
consumers, in 24 files, and nothing checks shape."* That item was filed as needing a **preference**.
It did not need one. It is measurable, and this is the measurement.

**Range.** `v1.17.0` (`7ff76b30`) `..` `HEAD` = `9a1f14a3`, measured on disk 2026-08-26.
The ledger measured the same question at `0a5323ab`; four more shape changes have landed since, so
its numbers and mine differ in a knowable way (§1).

**Method.** Every figure below was re-derived from git and from the parsed YAML. Every consumer was
**executed** against the current tree, and every consumer was **made to fail** — or is reported as
unable to fail, which is a finding rather than evidence of safety.

**Verdict up front: MEASURED-SAFE.** No consumer of the published set breaks on the new shapes.
The mixed state is **deliberate and rule-determined**, not drift (§4). Three pre-existing defects
were found on the way and are named in §5; none is caused by this release's reshaping, and none
blocks.

---

## 1 — The shape changes, derived

| Quantity | Ledger (`@0a5323ab`) | **Measured here (`@HEAD`)** |
|---|---|---|
| Top-level keys that changed YAML type | 30 | **34** |
| Files affected | "24" | **24** |
| `list → dict` | 21 | **23** |
| `str → dict` | 9 | **11** |

Command:

```bash
git archive v1.17.0 deliverables/ai/P2 | tar -x -C /tmp/old
git archive HEAD      deliverables/ai/P2 | tar -x -C /tmp/new
# then: yaml.safe_load every file at both revisions, compare type() of each top-level key
```

**Three disagreements with the ledger, all reproducible:**

1. **30 vs 34.** Re-running the identical measurement at the ledger's own revision `0a5323ab`
   reproduces **30** exactly. The ledger's key count was right when written. Four more landed after
   it: `architecture/debug_interrupt.yaml configuration`, `architecture/interrupts.yaml
   configuration_registers`, `hardware/addon-serial-host.yaml description`, and
   `hardware/edge-breadboard-carrier.yaml educational_value` (marked ⁺ in the table below).
2. **"24 files" was wrong at the time it was written.** At `0a5323ab` the true figure is **21**, and
   the ledger's own §1.10 table enumerates exactly those 21. It reads 24 today only by coincidence —
   the three files added since happen to close the gap.
3. **One of the 34 is not a reshape at all.** `hardware/edge-breadboard-carrier.yaml
   educational_value` was a **duplicate top-level key** at `v1.17.0` — a mapping at line 226 and the
   scalar `"excellent"` at line 257. YAML's last-wins rule made it parse as `str`. HEAD removed the
   shadowing scalar, so the mapping that was always in the file now parses. The type changed; nobody
   reshaped anything. It is the only one of the 34 with that origin, and the only one with no
   `source:` inside the block.

### The 34, enumerated

⁺ = landed after the ledger was written.
*load-bearing* = with its in-block `source:` deleted, `audit-yaml-claim-sourcing.py` fires Tier 1 on
that block (measured, §3 experiment E1).

| # | File (under `deliverables/ai/P2/`) | Top-level key | `v1.17.0` | HEAD | in-block `source:` | load-bearing for the armed gate |
|---|---|---|---|---|---|---|
| 1 | `application-notes/p2an001-single-pin-instrumentation-adc.yaml` | `gotchas` | `list` | `dict` | yes | no |
| 2 | `application-notes/p2an002-cordic-for-real-work.yaml` | `gotchas` | `list` | `dict` | yes | no |
| 3 | `application-notes/p2an004-frequency-rotation-rc-timing-measurement.yaml` | `gotchas` | `list` | `dict` | yes | no |
| 4 | `architecture/clock_system.yaml` | `configuration_rules` | `list` | `dict` | yes | **yes** |
| 5 | `architecture/debug_interrupt.yaml` ⁺ | `configuration` | `list` | `dict` | yes | no |
| 6 | `architecture/interrupts.yaml` ⁺ | `configuration_registers` | `list` | `dict` | yes | no |
| 7 | `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `operation` | `str` | `dict` | yes | **yes** |
| 8 | `architecture/smart-pins/smart-pin-00011-dac-16bit-pwm-dither.yaml` | `pwm_characteristics` | `str` | `dict` | yes | **yes** |
| 9 | `hardware/addon-av-breakout.yaml` | `signal_map` | `list` | `dict` | yes | **yes** |
| 10 | `hardware/addon-control-board.yaml` | `signal_map` | `list` | `dict` | yes | **yes** |
| 11 | `hardware/addon-hd-audio.yaml` | `description` | `str` | `dict` | yes | no |
| 12 | `hardware/addon-motor-driver.yaml` | `signal_map` | `list` | `dict` | yes | **yes** |
| 13 | `hardware/addon-rtc.yaml` | `description` | `str` | `dict` | yes | no |
| 14 | `hardware/addon-rtc.yaml` | `pin_mode_tip` | `str` | `dict` | yes | no |
| 15 | `hardware/addon-serial-device.yaml` | `description` | `str` | `dict` | yes | **yes** |
| 16 | `hardware/addon-serial-device.yaml` | `signal_map` | `list` | `dict` | yes | **yes** |
| 17 | `hardware/addon-serial-host.yaml` ⁺ | `description` | `str` | `dict` | yes | **yes** |
| 18 | `hardware/addon-serial-host.yaml` | `development_workflow` | `list` | `dict` | yes | **yes** |
| 19 | `hardware/addon-serial-host.yaml` | `signal_map` | `list` | `dict` | yes | **yes** |
| 20 | `hardware/addon-wx-wifi.yaml` | `pin_descriptions` | `list` | `dict` | yes | **yes** |
| 21 | `hardware/edge-32mb-module.yaml` | `development_workflow` | `list` | `dict` | yes | **yes** |
| 22 | `hardware/edge-32mb-module.yaml` | `limitations` | `list` | `dict` | yes | **yes** |
| 23 | `hardware/edge-breadboard-carrier.yaml` ⁺ | `educational_value` | `str` | `dict` | **no — not a reshape** | no |
| 24 | `hardware/hub75_adapter.yaml` | `description` | `str` | `dict` | yes | **yes** |
| 25 | `hardware/hub75_adapter.yaml` | `notes` | `list` | `dict` | yes | **yes** |
| 26 | `hardware/programming-prop-plug.yaml` | `description` | `str` | `dict` | yes | **yes** |
| 27 | `language/pasm2/concepts/streamer_smartpin_control.yaml` | `protocol_client_code_note` | `str` | `dict` | yes | no |
| 28 | `language/pasm2/setxfrq.yaml` | `common_values` | `list` | `dict` | yes | **yes** |
| 29 | `language/spin2/debug-commands/pc_key.yaml` | `usage_rules` | `list` | `dict` | yes | **yes** |
| 30 | `language/spin2/methods/waitms.yaml` | `limitations` | `list` | `dict` | yes | no |
| 31 | `language/spin2/methods/waitms.yaml` | `notes` | `list` | `dict` | yes | no |
| 32 | `language/spin2/methods/waitus.yaml` | `clock_frequency_impact` | `list` | `dict` | yes | no |
| 33 | `language/spin2/methods/waitus.yaml` | `limitations` | `list` | `dict` | yes | no |
| 34 | `language/spin2/methods/waitus.yaml` | `notes` | `list` | `dict` | yes | no |

---

## 2 — The mixed state, derived

The ledger's splits are right in the scope it meant and wrong KB-wide. Both are reported.

| Key | `v1.17.0` | HEAD | Ledger said |
|---|---|---|---|
| `signal_map` (KB-wide; all occurrences are in `hardware/`) | `list` ×14 | **`dict` ×5 · `list` ×10** | "mapping in 5 … list in 9" |
| `gotchas` (**KB-wide**) | **`dict` ×3 · `list` ×7** | `dict` ×6 · `list` ×4 | "at `v1.17.0` each of these was uniform" |
| `gotchas` (application-notes only) | `list` ×7 | `dict` ×3 · `list` ×4 | "mapping in 3 … list in 4" ✔ |
| `description` (`hardware/` only) | `str` ×20 | **`dict` ×8 · `str` ×14** | "mapping in 5 … string in 11" |

- `signal_map` **list ×10, not 9**: the tenth is `hardware/addon-click-adapter.yaml`, a file this
  release *added*, born with a list. The ledger's 9 counted only pre-existing files.
- **`gotchas` was already mixed at `v1.17.0`.** `language/spin2/operators/typed-pointers.yaml`,
  `language/spin2/keywords/STRUCT.yaml` and
  `architecture/smart-pins/smart-pin-11110-async-serial-transmit.yaml` were mappings before this
  release. The ledger's "at `v1.17.0` each of these was uniform" holds only if `gotchas` is scoped
  to application-notes; KB-wide it is false, and this release did not create that particular mixture.
- `description` **dict ×8, not 5**: six files reshaped (the ledger's table lists five and omits
  `addon-serial-host`, which was reshaped after the ledger was written) plus two new files born with
  a mapping (`addon-click-adapter`, `p2-package-mechanical`). The str side is **14**, not 11.

---

## 3 — Consumers: does it READ the key, does it TOLERATE it, and could it have failed

Every row was executed against the current tree. Mutation experiments ran in a `git clone --local`
of the repo at `9a1f14a3`; the working tree was never modified and `deliverables/ai/p2kb-index.json`
was never regenerated in place.

| Consumer | Reads the changed keys? | Command | Result | How it was made to fail |
|---|---|---|---|---|
| `engineering/tools/generate-p2kb-index.py` | **No** | run in a clone, then re-run with `signal_map` flipped `dict→list` in the 5 hardware files and `gotchas` flipped in the 3 app-notes | **exit 0; the emitted index is identical field-for-field** (1133 entries / 2082 aliases both runs; zero differing `files` entries) | **Yes.** `aliases:` `list→dict` in one file → 18 aliases vanish (2082→2062). It *is* shape-sensitive on the four keys it reads (`aliases`, `pattern_id`, `instruction`, `method`) — none of which is among the 34. |
| `engineering/tools/p2kb/fetch-kb-file.sh` (download-on-demand) | **No** — treats YAML as opaque text; strips 5 metadata line-patterns and cats the rest | real script, `BASE_URL` repointed to `file://` on the local tree, run for **all 24** reshaped files | **exit 0 for all 24; every delivered payload parses and carries the new shapes** (e.g. `signal_map` arrives as `{source, pins, usb_pin_pairing_note}`) | **Yes.** Added `shape_probe:` whose only child is `documentation_source:`. On disk it is a mapping; **as delivered by the script it is `null`.** The filter is indentation-blind, so it *can* destroy a block — it just isn't destroying any of these 34. |
| `engineering/tools/validate-crossref-keys.py` | **No** — none of the 18 distinct changed key names is in `CROSS_REF_FIELDS` | run against the real tree, and against the flipped clone | **exit 0 both times, byte-identical output** — including the `692 nested site(s) NOT checked` count, so no cross-reference site lives inside any reshaped block | **Yes, twice.** (a) a bogus `related:` target → exit 1. (b) `related:` `list→dict` in `language/pasm2/add.yaml` → `related: 1862 resolved` drops to `1858`, a spurious unresolved `"items"` appears, exit 1. It is fully shape-sensitive on the keys it reads. |
| `engineering/tools/validation/audit-yaml-claim-sourcing.py` | **YES** — the only consumer that does. It walks *every* top-level block by line indentation, so all 34 are in scope | `--inventory` on the real tree | **exit 0** — Tier 1 = 0 across 1133 files, Tier 2 = 49 advisory | **Yes, three ways.** Built-in `--negative-control`: 40 cases, all pass. **E1**: delete the in-block `source:` from all 33 real reshapes → **exit 1, 19 Tier 1 violations**, Tier 2 rises 49→52. **E2**: move that same `source:` out to a top-level sibling `<key>_source:` → **exit 1, 22 Tier 1 violations**, all 19 originals still firing. |
| p2kb-mcp fetch contract (`engineering/tools/p2kb-mcp/P2KB-MCP-SPECIFICATION.md`) | **No** — content is returned as an opaque filtered string; the only YAML parsing in the contract is `p2kb_related`, which reads `related_instructions` | `p2kb_version` + `p2kb_get p2kbHwAddonSerialHostAddonSerialHost`; then the recorded Go `FilterMetadata` regex transcribed verbatim and run over all 1133 current files | The **deployed** server serves the *published* set — index 3.5.0, **1129 entries**, i.e. `v1.17.0`-era; it returned `addon-serial-host` with `signal_map` still a list. It has not seen these shapes yet. The **recorded contract**, run over the current tree: 1698 lines stripped, **0 payloads fail to parse, 0 top-level keys change type**. | **Yes** — the same `shape_probe` control run through the Go regex transcription: mapping in, `null` out. |

`validate-dod-release.py` runs all 11 checks green (`Fetch Script Parity: PASS`, v3.4 both scripts,
5 filter fields, base URLs, 86400 s).

### Why the two "no" answers are evidence and not silence

For `generate-p2kb-index.py` and `validate-crossref-keys.py` the claim is not merely "it exited 0".
Both were **shown to notice a shape change** on a key they *do* read — the index generator loses 18
aliases when `aliases:` becomes a mapping; the cross-reference validator loses 4 resolutions and
goes red when `related:` becomes a mapping. Both then produced **identical output** when the actual
34 keys were flipped. That pair — sensitive on what it reads, identical on what changed — is what
makes the null result mean something.

The fetch script and the MCP contract are different in kind: they never parse YAML, so they cannot
have an opinion about `list` vs `dict`. What they *can* do is corrupt a block whose only child is a
metadata-named key, and the `shape_probe` control proves it. None of the 34 nests such a key, so
neither path is affected.

---

## 4 — Is the mixture deliberate?

**Deliberate, and determined by a rule that can be stated exactly.**

E2 is the decisive experiment. The ledger names an alternative that would have kept the shapes
uniform — *"a sibling `signal_map_source:` key"*. That alternative was measured: with the citation
moved from inside each block to a top-level sibling, `audit-yaml-claim-sourcing.py` returns **exit 1
with 22 Tier 1 violations, including all 19 of the blocks the in-block form silences.** The
uniform-shape alternative does not satisfy the armed gate. The reshape was **forced by the
instrument**, not chosen for taste.

The boundary of the mixture is the boundary of the instrument's demand. For every block still
carrying the old shape — `signal_map` list ×10, `gotchas` list ×4 (app-notes), `description` str ×14
(hardware) — the question *"would the gate demand a reshape here?"* was evaluated with the auditor's
own `top_level_blocks` / `quantities_in` / `cites_in`:

**0 of 28.** Every one of them either states no physical quantity in that block, or already carries
an in-block citation in its prose. Not one is a block that got away.

So: **reshaped ⟺ the block stated an uncited quantity inside a file that demonstrably cites.** The
converse is looser — 19 of the 33 real reshapes are load-bearing today; the other 14 were done for
consistency inside files that were being edited anyway. That asymmetry is worth knowing, but it is
consistency-with-a-rule, not drift.

**What this does not settle.** The rule is real but nothing enforces it, and nothing records it in
the tree. The next block that acquires a quantity will drift the shape further, and the only thing
that would catch it is the citation gate firing — which fixes citation, not uniformity. If a
schema is ever wanted, this is the rule to write down. That is a separate decision and it is not
blocking: no consumer is affected today.

---

## 5 — Three defects found on the way (none caused by this release)

1. **`generate-p2kb-index.py` cannot fail on a broken file.** Its alias harvest ends in
   `except Exception: pass` (≈ line 116). A file made syntactically invalid was still indexed with a
   path and a sha256, lost its `MOV` alias silently, and the run **exited 0 printing nothing**. A
   green run of the index generator is not evidence that the corpus parses.
   `python3 engineering/tools/verify-yaml-format.py` is the tool that actually answers that (exit 0
   over 1133 files today), and it must not be assumed to be covered by the generator.

2. **`validate-dod-release.py`'s Metadata Filter check reads which lines were removed, never
   whether the payload survived.** It applies the filter and classifies the removed lines against
   the 5 expected fields (lines 352-396) but never re-parses the result. The `shape_probe` failure —
   a mapping delivered as `null` — passes that check untouched. Making it re-parse the filtered
   payload and compare top-level types would close it; the sweep run here shows the corpus is clean
   today (0 of 1133).

3. **The download-on-demand filter silently deletes a real citation, in one file, today.**
   Seven files in the corpus carry a filtered-key name at a **nested** indent, and six of them are
   an innocuous `last_updated:`. The seventh is not:
   `language/spin2/statements/debug.yaml:16` holds
   `window_name_rules.documentation_source:` — a citation naming PNut v55 compiler source lines and
   a hardware-isolation date. Both the fetch script and the recorded MCP filter strip it, so every
   agent that fetches `p2kbSpin2Debug` receives that block **with its provenance removed**. The
   block still parses (it has other children), which is why nothing has noticed.
   Pre-existing — present unchanged at `v1.17.0` — and **not** one of the 34. It is recorded here
   because this sweep is what found it, and because it is exactly the hazard §1.10 feared: had any
   reshape reached for `documentation_source:` instead of `source:`, the citation it was added to
   carry would have been deleted in delivery.
   `grep -nE '^[ \t]+(last_updated|enhancement_source|documentation_source|documentation_level|manual_extraction_date):' -r deliverables/ai/P2`

---

## 6 — Commands, for re-running

```bash
# the 34 shape changes.  These once ran as `git -c safe.directory=$PWD ...`; that workaround is
# retired — /etc/gitconfig carries safe.directory=/workspaces/* at system scope (8778e6a2).
# Do not re-add it.
git archive v1.17.0 deliverables/ai/P2 | tar -x -C /tmp/old
git archive HEAD      deliverables/ai/P2 | tar -x -C /tmp/new
# compare type() of each top-level key of each file across the two trees

# consumers, current tree
python3 engineering/tools/verify-yaml-format.py                             # exit 0, 1133 files
python3 engineering/tools/validate-crossref-keys.py                         # exit 0
python3 engineering/tools/validation/audit-yaml-claim-sourcing.py --inventory# exit 0, Tier1=0
python3 engineering/tools/validation/audit-yaml-claim-sourcing.py --negative-control
python3 engineering/tools/validate-dod-release.py                           # exit 0, 11 checks

# fetch script against the local tree (real script, BASE_URL -> file://)
sed -i 's|^BASE_URL=.*|BASE_URL="file://'"$PWD"'"|' /tmp/ft/fetch-kb-file.sh
bash /tmp/ft/fetch-kb-file.sh p2kbHwAddonSerialHostAddonSerialHost | python3 -c \
  'import sys,yaml; d=yaml.safe_load(sys.stdin); print(type(d["signal_map"]).__name__)'   # dict

# mutation experiments (in a clone; never in the working tree)
git clone --local --shared . /tmp/clone
```

**Index discipline.** `generate-p2kb-index.py` was run only inside `/tmp/clone`. The repo's
`deliverables/ai/p2kb-index.json` and `.json.gz` were never touched; `git status` is clean.
