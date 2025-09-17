-- P2KB Non-Floating Images Lua Filter
-- Ensures images are placed exactly where they appear in markdown (no floating)
-- Author: Iron Sheep Productions, LLC
-- Version: 1.1 - Fixed caption handling for Block elements
-- Used by: Debug Window Manual for screenshot placement

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
    -- Fix: Use title attribute instead of caption to avoid Block/Inline issues
    if elem.title and elem.title ~= "" then
        latex_code = latex_code .. string.format("\\caption{%s}\n", elem.title)
    elseif elem.attributes.caption then
        latex_code = latex_code .. string.format("\\caption{%s}\n", elem.attributes.caption)
    end
    
    latex_code = latex_code .. "\\end{figure}"
    
    return pandoc.RawBlock("latex", latex_code)
end