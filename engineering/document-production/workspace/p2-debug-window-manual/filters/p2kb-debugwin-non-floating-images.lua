-- P2KB Debug Window Non-Floating Images Lua Filter
-- Ensures images are placed exactly where they appear in markdown (no floating)
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - Debug Window specific version with caption fix
-- Based on: p2kb-non-floating-images.lua (shared version)

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
    -- Debug Window fix: Use title attribute to avoid Block/Inline issues
    if elem.title and elem.title ~= "" then
        latex_code = latex_code .. string.format("\\caption{%s}\n", elem.title)
    elseif elem.attributes.caption then
        latex_code = latex_code .. string.format("\\caption{%s}\n", elem.attributes.caption)
    end
    
    latex_code = latex_code .. "\\end{figure}"
    
    return pandoc.RawBlock("latex", latex_code)
end