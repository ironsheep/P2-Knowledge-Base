-- P2KB PASM2 Entry Header Color Bar Lua Filter
-- Converts div-syntax entry headers to LaTeX color bar environments
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - Entry Type Color Bar Processing
--
-- Handles three entry types:
--   ::: instrheader   -> \begin{instrheader}...\end{instrheader}  (Brick Red bar)
--   ::: dirheader     -> \begin{dirheader}...\end{dirheader}      (Amber bar)
--   ::: constheader   -> \begin{constheader}...\end{constheader}  (Violet bar)

-- Convert div blocks to appropriate LaTeX environments
function Div(elem)
    local class = elem.classes[1]

    -- Instruction entry header (Brick Red #C62828)
    if class == "instrheader" then
        return {
            pandoc.RawBlock("latex", "\\begin{instrheader}"),
            elem,
            pandoc.RawBlock("latex", "\\end{instrheader}")
        }

    -- Directive entry header (Amber #FF8F00)
    elseif class == "dirheader" then
        return {
            pandoc.RawBlock("latex", "\\begin{dirheader}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dirheader}")
        }

    -- Constant entry header (Violet #8E24AA)
    elseif class == "constheader" then
        return {
            pandoc.RawBlock("latex", "\\begin{constheader}"),
            elem,
            pandoc.RawBlock("latex", "\\end{constheader}")
        }
    end

    -- Return unchanged if not a recognized entry header type
    return elem
end
