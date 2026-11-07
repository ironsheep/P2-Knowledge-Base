# P2KB contract gaps: manual reach notes

**For:** `P2KB-CONTRACT-GAPS-SPRINT-PLAN.md` §13. **Started:** 2026-11-07.

Stephen, 2026-11-07: *"complete the YAML edits for all of what we're trying to do, then, in a focused
effort, apply the YAML changes to all the manuals … You see that a manual is affected by an edit. You
can start taking notes on which manuals are affected."*

**How this file is kept.** When a YAML fix is made and a manual master is seen to carry the same claim,
a row is added here at that moment. Nothing here is edited in a master during the YAML work. The
focused manual effort that follows the KB release works from this list.

Master paths are under each manual's `opus-master/` folder in
`engineering/document-production/manuals/<slug>/`.

| YAML change (plan §) | Manual | Master file:line | What the master says |
|---|---|---|---|
| BRK bit order (§1) | Assembly Language Reference | `part-ii/instructions-b.md:311` | The old bit order |
| TRGINT under STALLI (§1, arm H) | Assembly Language Reference | `part-ii/instructions-t.md:434,448`; `part-iii/appendix-c-categorical-index.md:443-445` | "Regardless of STALLI mode" |
| Q is read with MUXQ (§17.2) | Assembly Language Reference | `part-ii/special-registers.md:501` | "Write-only … no instruction reads it back" |
| XBYTE flags from the index (§1, §5) | XBYTE guide | `xbyte-body.md:822,1113` | "Writes the bytecode's own low bits into C and Z"; `:917` already says "bytecode index" |
