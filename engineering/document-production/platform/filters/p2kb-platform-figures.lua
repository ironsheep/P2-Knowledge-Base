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
--   \caption{Caption Text Here}
--   \label{fig:some-id}
--   \end{figure}
--
-- Version: 1.2
-- Date: 2026-06-06
-- Implements: Rayman review item C1 (figure numbering)
-- v1.1: Use \caption*{} for hardcoded figure numbers (no auto-numbering)
-- v1.2: Switch to NUMBERED \caption{} (layout standard). The figurecaption div
--       carries bare caption text (no "Figure N" prefix), so \caption auto-numbers
--       as "Figure C.N" (chapter-scoped via \counterwithin in foundation) AND
--       registers the figure in the List of Figures. The div is already
--       consolidated into this single caption -- there is no separate rendering.

-- A "bold lead-in" is a short paragraph that is a single bold run -- a label like
-- **Immediate -> LUT -> Pins/DACs:** that introduces the table directly below it.
-- (Every top-level inline is Strong/Space/SoftBreak, at least one Strong, and the
-- whole thing is short.) Ordinary prose that merely contains a bold word is NOT a
-- lead-in (it has Str inlines outside the Strong).
local function is_bold_leadin(blk)
  if blk.t ~= "Para" and blk.t ~= "Plain" then return false end
  if #pandoc.utils.stringify(blk.content) > 60 then return false end
  local seen_strong = false
  for _, il in ipairs(blk.content) do
    if il.t == "Strong" then
      seen_strong = true
    elseif il.t == "Space" or il.t == "SoftBreak" then
      -- allowed (surrounding/trailing space)
    else
      return false
    end
  end
  return seen_strong
end

-- Count data rows in a pandoc Table element (excluding the header row).
local function table_data_rows(t)
  local n = 0
  if t.bodies then
    for _, b in ipairs(t.bodies) do
      if b.body then n = n + #b.body end
    end
  end
  return n
end

-- A "code box" block: a fenced CodeBlock, or a Div wrapping one (::: pasm2 etc.).
-- These become the colored code boxes (IOSPBlock/Spin2Block/...) in
-- p2kb-platform-code-coloring.lua, which runs AFTER this filter -- so here they
-- are still CodeBlock / Div elements.
local CODE_DIV_CLASSES = {
  pasm2 = true, spin2 = true, iosp = true, pasm = true,
  cordic = true, multicog = true, antipattern = true,
}
local function is_code_box(blk)
  if blk.t == "CodeBlock" then return true end
  if blk.t == "Div" and blk.classes then
    for c in pairs(CODE_DIV_CLASSES) do
      if blk.classes:includes(c) then return true end
    end
  end
  return false
end

-- Line count of the code inside a code-box block (sizes the needspace reserve).
local function code_box_lines(blk)
  local cb = nil
  if blk.t == "CodeBlock" then
    cb = blk
  elseif blk.t == "Div" then
    pandoc.walk_block(blk, { CodeBlock = function(c) cb = c; return c end })
  end
  if not cb then return 1 end
  local n = 1
  for _ in cb.text:gmatch("\n") do n = n + 1 end
  return n
end

-- Process blocks to find RawBlock + figurecaption Div pairs, AND bold-lead-in +
-- table pairs (keep the label welded to its table). Runs before the table filter,
-- so the table is still a pandoc Table element here (row count is available).
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
                          "\\caption{" .. caption_text .. "}\n"

      -- Add label if present
      if label_id ~= "" then
        figure_latex = figure_latex .. "\\label{" .. label_id .. "}\n"
      end

      figure_latex = figure_latex .. "\\end{figure}"

      -- Insert the combined figure block
      table.insert(result, pandoc.RawBlock("latex", figure_latex))

      -- Skip both the RawBlock and the Div (advance by 2)
      i = i + 2
    elseif is_bold_leadin(current) and next_block and next_block.t == "Table" then
      -- Keep a bold lead-in label welded to the table it introduces: reserve space
      -- for the label + table so a page break moves the whole unit instead of
      -- stranding the label at the page foot (Ch 13.1 / 14.2 symbol tables). Size
      -- the reserve to the table's height (data rows + header + label line), capped
      -- so a very tall table -- which the table filter makes breakable anyway --
      -- never over-reserves and forces a needless early break.
      local n = table_data_rows(next_block) + 4
      if n > 28 then n = 28 end
      table.insert(result, pandoc.RawBlock("latex",
        string.format("\\needspace{%d\\baselineskip}", n)))
      table.insert(result, current)
      i = i + 1
    elseif is_bold_leadin(current) and next_block and is_code_box(next_block) then
      -- Keep a bold lead-in label welded to the code box it introduces (e.g.
      -- "**PASM2 Example:**" directly above a ```pasm2 block): reserve space for
      -- the label + the box so a page break moves the whole unit instead of
      -- stranding the label at the page foot (I/O "Document Conventions" p14).
      -- Sized to the code's line count (+ a few lines for the box padding /
      -- before-skip), capped so a long breakable box -- which splits across pages
      -- anyway -- never over-reserves and forces a needless early break.
      local n = code_box_lines(next_block) + 3
      if n > 14 then n = 14 end
      table.insert(result, pandoc.RawBlock("latex",
        string.format("\\needspace{%d\\baselineskip}", n)))
      table.insert(result, current)
      i = i + 1
    else
      -- Not a figure or lead-in pattern, keep the block as-is
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
  -- When that header is the bottom of a run of IMMEDIATELY-consecutive headers
  -- (e.g. a \section directly above the \subsection that introduces the diagram),
  -- mark the OUTERMOST header of the run so the reserve sits before the WHOLE
  -- heading stack -- otherwise the big reserve lands between the headings and the
  -- outer one is stranded alone at the page foot (I/O Ch1 "1.2 Timing").
  local function reserve_before_heading(i, lookback, frac)
    local back = 0
    for j = i - 1, 1, -1 do
      back = back + 1
      if blocks[j].t == "Header" then
        local k = j
        while k - 1 >= 1 and blocks[k - 1].t == "Header" do k = k - 1 end
        mark(k, frac)
        return
      end
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
    local prev_is_header = (i > 1 and blocks[i - 1].t == "Header")
    if needs_reserve[i] then
      table.insert(out, pandoc.RawBlock("latex",
        string.format("\\needspace{%.2f\\textheight}", needs_reserve[i])))
    elseif b.t == "Header" and b.level and b.level >= 2 and b.level <= 4
           and not prev_is_header then
      -- Orphan-heading guard, STACK-AWARE: reserve space before a section /
      -- subsection / subsubsection heading so a heading near the page bottom moves
      -- to the next page WITH its first lines of content instead of being stranded
      -- at the foot. When a heading sits directly above more headings (section ->
      -- subsection), the reserve must cover the WHOLE run + a couple of body lines
      -- and be emitted ONCE before the run's first heading -- otherwise the outer
      -- heading places, then an inner heading's own guard breaks the page and
      -- strands the outer one (I/O §8.5 "Analog Output with DAC"). Inner headers
      -- (prev_is_header) get no guard. Small fixed reserve (not a \textheight
      -- fraction) so it never gaps the page like the diagram/table reserves above.
      local run = 1
      local j = i + 1
      while blocks[j] and blocks[j].t == "Header" do run = run + 1; j = j + 1 end
      local n = run * 2 + 2          -- ~2 lines per heading in the run + ~2 body lines
      if n > 10 then n = 10 end
      table.insert(out, pandoc.RawBlock("latex",
        string.format("\\needspace{%d\\baselineskip}", n)))
    end
    table.insert(out, b)
  end
  doc.blocks = out
  return doc
end
