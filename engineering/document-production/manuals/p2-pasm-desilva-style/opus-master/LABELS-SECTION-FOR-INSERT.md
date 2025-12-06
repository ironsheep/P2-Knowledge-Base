## Labels: Naming Your Places

You've been using labels throughout this chapter without us properly introducing them. How rude of me! Let's fix that.

### Global Labels: The Big Signposts

A global label is just a name at the start of a line:

::: pasm2
```
DAT             org

send_byte       rdbyte  x, ptr          ' Global label
                wypin   x, tx_pin
                ret

receive_byte    testp   rx_pin    wc    ' Another global label
                rdpin   x, rx_pin
                ret
```
:::

Global labels are visible everywhere in your DAT block. You can jump to them, call them, reference them from Spin2 - they're your main signposts.

### Local Labels: The Little Helpers

But here's a problem. What if every routine needs a loop? You can't have two labels called `loop` - the assembler would be terribly confused.

Enter local labels. Prefix a name with a dot (`.`) and it becomes local:

::: pasm2
```
DAT             org

send_byte       rdbyte  x, ptr
.loop           testp   tx_pin    wc    ' Local: belongs to send_byte
        if_nc   jmp     #.loop
                wypin   x, tx_pin
                ret

receive_byte    testp   rx_pin    wc    ' New scope begins here
        if_nc   jmp     #.wait
.wait           testp   rx_pin    wc    ' Local: belongs to receive_byte
        if_nc   jmp     #.wait
                rdpin   x, rx_pin
.loop           shr     x, #24          ' Different .loop - no conflict!
                ret
```
:::

Each global label starts a new "scope". The `.loop` under `send_byte` is completely separate from the `.loop` under `receive_byte`. You can reuse `.loop`, `.done`, `.retry`, `.exit` to your heart's content.

### The Colon Alternative

You might also see local labels with a colon prefix:

::: pasm2
```
:loop           djnz    count, #:loop   ' Same as .loop
```
:::

Both `:` and `.` work identically. I prefer the dot - it's what modern convention has settled on - but you'll see both in the wild.

### Reference Operators: Finding Your Labels

When you reference a label, you need to tell the assembler what you want:

::: pasm2
```
' In COG code (after ORG):
        jmp     #my_routine     ' # = immediate COG address
        call    #.helper        ' # works for local labels too
        mov     x, #data_table  ' Get COG address of data

' For hub addresses (used with Spin2):
        mov     ptr, @hub_data  ' @ = hub address of label
```
:::

The `#` means "immediate value" - use this for jumps and calls within COG code. The `@` means "hub address" - use this when passing addresses to Spin2 or for hub memory operations.

### Scope Boundaries: When Local Labels Reset

Here's the rule: **every global label or data definition starts a new local scope**.

::: pasm2
```
func_a          mov     x, #1           ' Scope #1 begins
.loop           djnz    x, #.loop       ' .loop in scope #1

data_block      long    0, 0, 0, 0      ' Scope #2 begins (data counts!)

func_b          mov     y, #2           ' Scope #3 begins
.loop           djnz    y, #.loop       ' .loop in scope #3 - different!
.done           ret
```
:::

This is wonderfully useful - your utility routines can all use `.loop` and `.done` without stepping on each other's toes.

### The Medicine: Quick Reference

| What | Syntax | Example |
|------|--------|---------|
| Global label | `name` | `my_routine` |
| Local label | `.name` or `:name` | `.loop`, `:done` |
| Jump to label | `#label` | `jmp #.loop` |
| Hub address | `@label` | `mov ptr, @data` |

### Common Gotchas

1. **Forgetting the dot**: `loop` is global, `.loop` is local. If you accidentally create a global `loop`, you'll get conflicts.

2. **Scope surprise**: Data definitions (`LONG`, `WORD`, `BYTE`) also start new scopes. If you put data between two parts of a routine, your local labels won't work!

3. **The 30-character limit**: For compatibility with all tools, keep label names under 30 characters. `this_is_a_really_long_label_name` might cause trouble.

