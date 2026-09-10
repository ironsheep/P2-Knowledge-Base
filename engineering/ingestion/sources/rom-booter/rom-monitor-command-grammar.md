# P2 ROM Monitor — Complete Command Grammar

**Extracted:** 2026-09-10
**Source:** `rom_booter_v33_01j.lst` — the **silicon** build (`ver = "G"`, *Prop2 Silicon v2*).
Command loop `_HubMonitor` at `$FCD78`; dispatch at listing lines 2079–2101.

> This closes the `p2-monitor.yaml` knowledge gap recorded in
> `sources/taqoz/taqoz-content-gaps-and-grounding-plan.md`: *"full command grammar beyond the
> 2 Datasheet examples; modify-command syntax."* Read from the ROM itself, not from web research.

## The line format

```
[xxxxxx]<cmd>
```

The Monitor reads a `<cr>`-terminated line, then `_ParseHex` (`$FCF70` region) consumes an
**optional leading hex value** and returns four things — the listing states them in a comment
block at line 2084:

```
returns: lmm_x = addr(hex), lmm_c = digitcount, lmm_p = ptr-next-char
         lmm_w = next non-hex char with lcase converted to ucase
```

Two consequences worth documenting, both read off that one comment:

- **Commands are case-insensitive.** The parser upper-cases the command character before it is
  compared, so `g` and `G` are the same command.
- **The digit COUNT is semantic, not just the value.** `lmm_c` is tested against 4 to decide
  cog/LUT versus hub addressing — `_Download` does `cmp lmm_c,#4 wc` and, when there are 4 or
  more digits, sets bit 31 of the address to mark it *hub* (`if_nc bith lmm_p2,#31`, line 2205).
  So `100:` and `0100:` are **not** the same target.

## The commands

Dispatch order is the listing's own: commands that take no address are tested first.

### Without an address

| Key | Handler | What it does |
|---|---|---|
| `<cr>` | `_Cmd_CR` `$FCDCC` | Repeat the previous LIST |
| `<esc>` (`$1B`) | `_Enter_TAQOZ` `$FD02C` | Enter the TAQOZ Forth interpreter |
| `L` | `_Cmd_Run` `$FCE54` | **L**oad a file — `L<filename.xtn><cr>` — load without running |
| `R` | `_Cmd_Run` `$FCE54` | **R**un a file — `R<filename.xtn><cr>` — load and run |
| `Q` | (returns) | QUIT — returns to the caller |

`_TAQOZ_ = $1B` is declared at line 837 with the comment `' <esc>   goto TAQOZ`.
`L` and `R` share one handler; it saves the key (`mov lmm_f, lmm_w`) and branches on it, which
is how one routine serves both.

### With an optional `{addr}` prefix

| Key | Handler | Form | What it does |
|---|---|---|---|
| `-` | `_Cmd_List` `$FCDF0` | `[addr]-` | LIST memory. Saves `{addr}`, zeroes `{addr2}`, and tests `digitcount < 4` to choose the address space |
| `:` | `_Download` `$FCEA4` | `[addr]:<hex> <hex> …` | **Download — this is the modify command.** Takes the address, then loops on `_ParseHex` consuming successive hex values and writing them |
| `G` | `_Cmd_G` `$FCE30` | `xxxxxxG<cr>` | GOSUB a cog / LUT / hub address. The listing's own comment. It special-cases `$FC000` — `cmp lmm_x, ##$FC000 wz` — as *"a ROM reboot"* |

### Anything else

`_Cmd_What` (`$FCDBC`) emits `"?"` followed by CR/LF and returns to the command loop.

## The modify-command answer

The grounding plan asked specifically for *"modify-command syntax."* It is **`:`** — the
Download command. There is no separate examine-and-alter command in this ROM: memory is changed
by downloading hex values to an address, and read back with `-` (LIST). That is the whole
write path, and it is worth stating plainly because a reader expecting a classic monitor's
`addr/value` modify syntax will look for one that does not exist.

## What this does NOT establish

- **No per-command operand grammar beyond what the dispatch and each handler's first
  instructions show.** LIST's second address (`lmm_lp2`) is initialised to zero and there is a
  `_HubListA2H` entry point, which together imply a range form — but this document does not
  assert its syntax, because that requires reading the LIST handler to its end rather than its
  head.
- **No claim that this grammar matches any other P2 monitor**, including the two examples in
  the Datasheet. Those should be re-checked *against* this table, not merged with it.
- Nothing here describes TAQOZ's own command set once `<esc>` hands over — that is the
  dictionary, catalogued in `taqoz-rom-dictionary.md`.
