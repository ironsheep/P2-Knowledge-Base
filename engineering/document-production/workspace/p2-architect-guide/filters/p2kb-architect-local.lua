-- p2kb-architect-local.lua — The P2 Architect's Guide per-manual Lua filter
--
-- The ONE architect-specific transform: a `::: p1note` fenced div becomes a
-- P1NoteBlock tcolorbox (defined in templates/p2kb-architect-local.sty; sprint DD1).
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

-- ============================================================================
-- Inline callout icons (AG-14). The prose uses two emoji markers that IBM Plex
-- cannot render (they come out as tofu boxes). Convert them to the fontawesome
-- macros defined in templates/p2kb-architect-local.sty (\WatchoutIcon / \TipIcon,
-- each with a plain-text fallback if fontawesome5 is absent).
--
-- WHY here and not an inline `\Macro`{=latex} span in the markdown: the
-- latex-escape pre-pass mangles inline raw-LaTeX attributes (`...`{=latex} ->
-- `...`\{=latex\}), which breaks them. Emoji, by contrast, pass the escape pass
-- untouched, and this filter runs after parsing — so we emit clean RawInline
-- LaTeX from the emoji here. (Handles the U+FE0F variation selector too.)
-- ============================================================================
function Str(elem)
  local t = elem.text
  if t == "⚠️" or t == "⚠" then
    return pandoc.RawInline('latex', '\\WatchoutIcon{}')
  elseif t == "💡" then
    return pandoc.RawInline('latex', '\\TipIcon{}')
  end
  return nil
end
