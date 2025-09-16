-- P2KB Non-Floating Images Lua Filter
-- Ensures images are placed exactly where they appear in markdown (no floating)
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - Standard image placement utility

-- Process images to prevent floating and set consistent sizing
function Image(elem)
    -- Default to 85% width for consistent sizing
    local width = "0.85\\textwidth"
    
    -- Check if width is already specified in attributes
    if elem.attributes.width then
        width = elem.attributes.width
    end
    
    -- Create LaTeX code for non-floating image placement
    local latex_code = string.format(
        "\\begin{figure}[H]\n\\centering\n\\includegraphics[width=%s]{%s}\n",
        width, elem.src
    )
    
    -- Add caption if present
    if elem.caption and #elem.caption > 0 then
        local caption_text = pandoc.utils.stringify(elem.caption)
        latex_code = latex_code .. string.format("\\caption{%s}\n", caption_text)
    end
    
    latex_code = latex_code .. "\\end{figure}"
    
    return pandoc.RawBlock("latex", latex_code)
end