-- P2KB PASM2 Reference Manual - Figure Caption Filter
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
-- Version: 1.0
-- Date: 2026-01-20
-- Implements: Rayman review item C1 (figure numbering)

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
    else
      -- Not a figure pattern, keep the block as-is
      table.insert(result, current)
      i = i + 1
    end
  end

  return result
end
