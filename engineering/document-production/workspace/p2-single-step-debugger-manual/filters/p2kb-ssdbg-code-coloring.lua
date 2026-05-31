-- P2KB Single-Step Debugger - Code Coloring Filter
-- Purpose: wrap language-tagged code fences in colored boxes matching the
--   PASM2 Assembly Reference / Smart Pins / IOSP scheme: Spin2 = blue,
--   PASM2 = green. Code is emitted inside a fancyvrb Verbatim so special
--   characters render literally and BLANK LINES ARE PRESERVED (the sibling
--   mnemonic-bold filters historically dropped blank lines inside code blocks;
--   this filter does NOT process line-by-line, so that bug cannot occur here).
-- Version: 1.0

-- Wrap a code block's text in a colored Verbatim box. block.text is used as-is
-- (no per-line loop), so interior blank lines survive intact.
local function wrap(text, env)
  return pandoc.RawBlock('latex',
    '\\begin{' .. env .. '}\n' ..
    '\\begin{Verbatim}\n' ..
    text .. '\n' ..
    '\\end{Verbatim}\n' ..
    '\\end{' .. env .. '}')
end

function CodeBlock(block)
  local c = block.classes
  if c:includes('spin2') or c:includes('spin') then
    return wrap(block.text, 'Spin2Block')
  elseif c:includes('pasm2') or c:includes('pasm') then
    return wrap(block.text, 'Pasm2Block')
  end
  -- untagged / other languages: leave for Pandoc's default handling
  return nil
end
