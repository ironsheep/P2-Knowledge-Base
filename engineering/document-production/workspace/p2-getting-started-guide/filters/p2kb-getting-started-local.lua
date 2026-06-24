-- p2kb-getting-started-local.lua — Getting Started with the Propeller 2 per-manual Lua filter
--
-- The ONE manual-specific transform: a `::: p1note` fenced div becomes a
-- P1NoteBlock tcolorbox (defined in templates/p2kb-getting-started-local.sty; sprint DD1).
-- Mirrors the platform prose-block pattern (tip/caution/hardware in
-- p2kb-platform-code-coloring.lua): wrap the div's child blocks in
-- \begin{P1NoteBlock} … \end{P1NoteBlock} as raw-LaTeX.
--
-- Registered AFTER the shared p2kb-platform-* filters in request.json, so the
-- platform code-coloring filter (which does NOT know the `p1note` class) has
-- already run and left this div untouched for us to convert.
--
-- Usage in the body:
--   ::: p1note
--   **P1 note:** … prose, lists, code fences all allowed …
--   :::

function Div(div)
  if div.classes:includes("p1note") then
    local result = { pandoc.RawBlock('latex', '\\begin{P1NoteBlock}') }
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{P1NoteBlock}'))
    return result
  end
  -- not ours — leave every other div unchanged
  return nil
end
