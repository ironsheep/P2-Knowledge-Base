-- P2KB IOSP Reference Manual - Figure Caption Filter
-- Purpose: Wraps TikZ diagrams with figure environments and captions
--
-- Input pattern in markdown:
--   ```{=latex}
--   \DiagramMacroName
--   ```
--
--   ::: {.figurecaption #fig:some-id}
--   Caption Text Here
--   :::
--
-- Output LaTeX:
--   \begin{figure}[H]
--   \centering
--   \DiagramMacroName
--   \caption*{Caption Text Here}
--   \label{fig:some-id}
--   \end{figure}
--
-- Version: 1.1
-- Date: 2026-01-23
-- Implements: Rayman review item C1 (figure numbering)
-- v1.1: Use \caption*{} for hardcoded figure numbers (no auto-numbering)

-- Process blocks to find RawBlock + figurecaption Div pairs
function Blocks(blocks)
  local result = {}
  local i = 1

  while i <= #blocks do
    local current = blocks[i]
    local next_block = blocks[i + 1]

    -- Check if current is a RawBlock (latex) and next is a figurecaption Div
    if current.t == "RawBlock" and
       current.format == "latex" and
       next_block and
       next_block.t == "Div" and
       next_block.classes and
       next_block.classes:includes("figurecaption") then

      -- Extract caption text from the Div content
      local caption_text = pandoc.utils.stringify(next_block.content)

      -- Extract the label ID (e.g., "fig:some-id")
      local label_id = next_block.identifier or ""

      -- Get the raw LaTeX content (the diagram macro)
      local diagram_latex = current.text

      -- Build the figure environment
      local figure_latex = "\\begin{figure}[H]\n" ..
                          "\\centering\n" ..
                          diagram_latex .. "\n" ..
                          "\\caption*{" .. caption_text .. "}\n"

      -- Add label if present
      if label_id ~= "" then
        figure_latex = figure_latex .. "\\label{" .. label_id .. "}\n"
      end

      figure_latex = figure_latex .. "\\end{figure}"

      -- Insert the combined figure block
      table.insert(result, pandoc.RawBlock("latex", figure_latex))

      -- Skip both the RawBlock and the Div (advance by 2)
      i = i + 2
    else
      -- Not a figure pattern, keep the block as-is
      table.insert(result, current)
      i = i + 1
    end
  end

  return result
end

-- Keep a diagram together with the heading + intro that introduce it.
-- Each diagram is a [H] figure (placed exactly here). When it doesn't fit on the
-- current page it jumps to the next, orphaning its section heading and intro
-- sentence at the bottom of the previous page. Reserving vertical space just
-- before that nearby heading forces the whole unit (heading + intro + figure) to
-- break to the next page together. We only reach back a few blocks so this
-- applies to the "heading -> short intro -> diagram" pattern, not to a diagram
-- that happens to sit far below an unrelated heading.
function Pandoc(doc)
  local blocks = doc.blocks
  local needs_reserve = {}   -- header index -> reserve fraction of \textheight

  -- Record the larger reserve when a header qualifies for more than one reason.
  local function mark(j, frac)
    if not needs_reserve[j] or frac > needs_reserve[j] then
      needs_reserve[j] = frac
    end
  end

  -- Walk back from block i to the nearest preceding Header within `lookback`.
  local function reserve_before_heading(i, lookback, frac)
    local back = 0
    for j = i - 1, 1, -1 do
      back = back + 1
      if blocks[j].t == "Header" then mark(j, frac); return end
      if back >= lookback then return end
    end
  end

  -- True if a Level-1 (chapter/appendix) header sits within `window` blocks
  -- before block i. Such a diagram/table is in the opening section of a chapter,
  -- which already starts on a fresh page (\clearpage), so it can never be
  -- orphaned -- reserving space there only pushes content down and leaves a
  -- blank gap after the section heading (the Ch 12.1 / 16.1 / Appendix B bug).
  local function near_chapter_start(i, window)
    for j = i - 1, math.max(1, i - window), -1 do
      if blocks[j].t == "Header" and blocks[j].level == 1 then
        return true
      end
    end
    return false
  end

  -- Table 1.10 (the tall instruction quick-reference) is the one wide table
  -- whose legend was orphaning. Match it by its header signature rather than a
  -- blanket row-count rule, so other long tables (e.g. the Appendix B mode
  -- list) do not get an unwanted near-full-page reserve.
  local function is_instruction_quickref(t)
    if not (t.head and t.head.rows and #t.head.rows > 0) then return false end
    local cells = t.head.rows[1].cells
    if not cells or #cells < 5 then return false end
    local h = {}
    for k = 1, #cells do h[k] = pandoc.utils.stringify(cells[k].contents):lower() end
    return h[1]:match("instruction") and h[3]:match("dir")
       and h[4]:match("out") and h[5]:match("flag")
  end

  for i, b in ipairs(blocks) do
    -- Diagrams: keep heading + intro + figure together, EXCEPT a diagram in a
    -- chapter's opening section (cannot be orphaned; reserve would gap the page).
    if b.t == "RawBlock" and b.format == "latex"
       and b.text:find("\\Diag", 1, true) then
      if not near_chapter_start(i, 10) then
        reserve_before_heading(i, 4, 0.30)
      end
    -- Table 1.10 only: keep heading + table + legend together.
    elseif b.t == "Table" and is_instruction_quickref(b)
           and not near_chapter_start(i, 10) then
      reserve_before_heading(i, 3, 0.72)
    end
  end

  local out = {}
  for i, b in ipairs(blocks) do
    if needs_reserve[i] then
      table.insert(out, pandoc.RawBlock("latex",
        string.format("\\needspace{%.2f\\textheight}", needs_reserve[i])))
    end
    table.insert(out, b)
  end
  doc.blocks = out
  return doc
end
