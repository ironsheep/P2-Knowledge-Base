# Interface Document Generator Guide

This document describes how the "Generate Documentation File" command works in the Spin2 VSCode extension. This command reads a `.spin2` or `.spin` source file and produces a `.txt` file containing the object's public interface — file-top documentation, a list of all PUB method signatures, and each PUB method's doc-comment documentation.

Understanding how comments are picked up (and what to avoid) is essential for producing clean, professional interface documents.

## Triggering the Generator

| Platform | Keybinding |
|---|---|
| macOS | `Ctrl+Alt+Cmd+D` |
| Windows/Linux | `Ctrl+Alt+D` |
| Command Palette | `Spin2: Generate Documentation File` |

The command is registered as `spinExtension.generate.documentation.file` and is implemented in `client/src/providers/spin.document.generate.ts` (`DocGenerator.generateDocument()`).

The generator produces a `{filename}.txt` file in the same directory as the source, then opens it beside the editor.

## What Is a "Doc Comment"?

The generator distinguishes between **doc comments** and **regular comments**. Only doc comments are included in the generated output.

| Comment Form | Doc Comment? | Included in Output? |
|---|---|---|
| `'' text` (double-tic, single line) | Yes | Yes |
| `{{ ... }}` (double-brace, multi-line) | Yes | Yes |
| `{{ text }}` (double-brace, single line — open and close on same line) | Yes | **No** — explicitly skipped |
| `' text` (single-tic, single line) | No | Never |
| `{ text }` (single-brace, single line) | No | Never |
| `{ ... }` (single-brace, multi-line) | No | Never |

**Key distinction:** `''` (double tic) is a doc comment. `'` (single tic) is not. Only double-tic and multi-line double-brace comments make it into the generated document.

## How the Generator Works (Two-Pass Process)

### Pass 1: File-Top Documentation + PUB Signature List

The first pass walks every line from top to bottom.

**File-top doc comments** are collected and emitted verbatim from the beginning of the file until the first PUB section is encountered:

- `''` lines: The text after `''` (from character position 2 onward) is written to the output. The `''` prefix is stripped. Blank `''` lines (just `''` with no following text) produce no output — not even a blank line.
- `{{ ... }}` multi-line blocks: Content is emitted line by line. On the opening `{{` and closing `}}` lines, text is emitted only if the trimmed line is longer than 2 characters. Interior lines are emitted as-is (trimmed).

**Important:** File-top doc comment collection does not stop at CON, VAR, OBJ, or DAT sections — it continues through them. It only stops when the first PUB is encountered. This means `''` doc comments inside a CON section that precedes the first PUB **will** appear in the file-top section of the generated document.

**At the first PUB**, the generator emits:
```
Object "{filename}" Interface:
  (Requires Spin2 Language v##)    ← only if {Spin2_v##} was found in file-top

PUB firstMethod(params) : returns
PUB secondMethod(params)
...
```

All PUB signatures are listed with comments and local variables stripped.

### Pass 2: PUB Method Details

The second pass walks every line again, this time emitting detailed documentation for each PUB method.

**For each PUB method**, the generator emits:
```
___________________________________
PUB methodName(params) : returns

 doc comment content here...
```

**Doc comments associated with a PUB method** are the `''` lines and `{{ }}` multi-line blocks that appear **after** the PUB declaration line, up until the next section start (PUB, PRI, CON, VAR, OBJ, or DAT).

**Trailing doc comment on the PUB line itself:** If the PUB declaration line contains `'' text` or `{{ text }}` after the signature, that text is also emitted as the first line of documentation for that method.

**PRI methods are excluded.** When a PRI section is encountered, doc comment collection is turned off. Doc comments inside PRI methods never appear in the output.

**After the last PUB method**, any trailing `''` or `{{ }}` doc comments at the end of the file are collected and appended to the output (as file-bottom documentation).

## The Language Version Spec

The generator hunts for `{Spin2_v##}` (e.g., `{Spin2_v44}`) in the file-top area. If found, it emits `(Requires Spin2 Language v##)` in the interface header. Versions below 43 are treated as 0 and not displayed. Hunting stops at the first section start line.

## Generated Output Structure

For a file with file-top docs and three PUB methods:

```
 File description line 1
 File description line 2

Object "myDriver" Interface:
  (Requires Spin2 Language v44)

PUB start(basePin, pinCount)
PUB configure(mode, value)
PUB getStatus() : status

___________________________________
PUB start(basePin, pinCount)

 Start the driver with given pins
 @param basePin - first pin to use
 @param pinCount - number of pins

___________________________
PUB configure(mode, value)

 Configure operating mode

__________________________
PUB getStatus() : status

 Return current status
 @returns status - current operating state

 File-bottom documentation here
```

## What to Do (Best Practices)

1. **Use `''` for all doc comments.** Double-tic is the primary doc comment form. It is reliable and well-supported by both the generator and the companion "Insert Doc Comment" command (`Ctrl+Alt+Cmd+C`).

2. **Place file-top documentation at the very top** of the file using `''` lines, before any section keywords if possible (though placement in early CON sections also works).

3. **Place method documentation immediately after the PUB line:**
   ```spin2
   PUB start(basePin, pinCount)
   '' Start the driver with given pins
   '' @param basePin - first pin to use
   '' @param pinCount - number of pins
   ```

4. **Use the Insert Doc Comment command** (`Ctrl+Alt+Cmd+C` on macOS) to auto-generate `''` comment stubs for PUB/PRI methods. For PUB methods, it uses `''` (doc comments) for the description, `@param`, and `@returns` lines, and `'` (non-doc) for local variables — correctly keeping locals out of the generated document.

5. **Use `'` (single-tic) for implementation notes** that should NOT appear in the interface document — internal explanations, TODOs, section separators within code, etc.

## What NOT to Do (Pitfalls)

### 1. Don't use single-line `{{ }}` for doc comments
```spin2
{{ This will NOT appear in the generated document }}
```
Single-line `{{ }}` (opening and closing on the same line) is explicitly skipped by the generator. Use `''` instead, or break it into a multi-line block.

### 2. Don't use `'` (single-tic) expecting it to appear in docs
```spin2
PUB start(pin)
' This will NOT appear in the generated document
```
Only `''` (double-tic) is a doc comment. Single `'` is an implementation comment.

### 3. Don't put section-organization comments in `''` between PUB methods
```spin2
PUB method1()
'' method1 documentation

'' ========== Motor Methods ==========

PUB method2()
```
The `'' ========== Motor Methods ==========` line will be captured as part of `method1`'s documentation, not as a standalone section header. Use `'` (single-tic) for organizational separators.

### 4. Don't put `''` comments in early CON/VAR/OBJ sections unless you want them in the doc
```spin2
'' File description
CON
  '' This note WILL appear in the file-top documentation
  MY_CONST = 5
PUB start()
```
File-top doc comment collection continues through CON, VAR, OBJ, and DAT sections until the first PUB is reached. Any `''` line before the first PUB ends up in the file-top area of the generated document.

### 5. Don't rely on blank `''` lines for spacing
```spin2
PUB start(pin)
'' Start the motor
''
'' More details here
```
A `''` line with no text after it (exactly 2 characters) produces **no output** — not even a blank line. If you need blank line spacing, use `''` followed by at least one space character (`'' `), or use a multi-line `{{ }}` block.

### 6. Don't expect PRI method documentation to appear
```spin2
PRI helper(x)
'' This will NOT appear in the generated document
```
The generator only includes PUB methods. PRI documentation is intentionally excluded from the public interface document.

### 7. Watch for `{Spin2_v##}` duplication
If `{Spin2_v44}` appears inside a `''` doc comment at the file top, it will show up twice — once as the literal text of the doc comment, and once in the `(Requires Spin2 Language v44)` header line. Place the version spec in a `{ }` non-doc comment instead:
```spin2
{Spin2_v44}
'' My driver description
```

### 8. Don't assume `{{ }}` content is emitted identically in all contexts
In file-top doc comments (pass 1), the `{{` and `}}` delimiter lines are trimmed. In PUB method doc comments (pass 2), leading whitespace is preserved on content lines. The closing `}}` line in pass 2 has its first 2 characters stripped, which may produce unexpected results if `}}` isn't at the start of the line.

## Related Commands

| Command | Keybinding (macOS) | Purpose |
|---|---|---|
| Generate Documentation File | `Ctrl+Alt+Cmd+D` | Produces the `.txt` interface document described above |
| Insert Doc Comment | `Ctrl+Alt+Cmd+C` | Inserts a `''` comment stub for the PUB/PRI method at cursor |
| Generate Hierarchy File | `Ctrl+Alt+Cmd+H` | Produces a `.readme.txt` showing the object dependency tree (unrelated to comments) |
