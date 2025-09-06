--[[
Green Book Semantic Blocks Lua Filter
Purpose: Convert markdown divs to LaTeX tcolorbox environments for semantic markers
Created: 2025-08-30
For: P2 Smart Pins Green Book Tutorial

Converts 7 semantic div types to corresponding LaTeX environments:
1. needs-diagram → needsdiagram
2. preliminary-content → preliminarycontent  
3. needs-verification → needsverification
4. needs-examples → needsexamples
5. needs-technical-review → needstechreview
6. needs-code-review → needscodereview
7. tip → tipbox
]]--

-- Mapping from div class names to LaTeX environment names
-- Using gb prefix to avoid pandoc conflicts
local divMappings = {
    ["needs-diagram"] = "gbdiagram",
    ["preliminary-content"] = "gbpreliminary",
    ["needs-verification"] = "gbverify",
    ["needs-examples"] = "gbexamples",
    ["needs-technical-review"] = "gbtechreview",
    ["needs-code-review"] = "gbcodereview",
    ["tip"] = "gbtip"
}

function Div(el)
    -- Check if div has classes
    if not el.classes or #el.classes == 0 then
        return el
    end
    
    -- Get the first class name
    local divClass = el.classes[1]
    
    -- Look up the corresponding LaTeX environment
    local envName = divMappings[divClass]
    
    if envName then
        -- Create LaTeX environment wrapper
        return {
            pandoc.RawBlock('latex', '\\begin{' .. envName .. '}'),
            el,
            pandoc.RawBlock('latex', '\\end{' .. envName .. '}')
        }
    end
    
    -- Return unchanged if not a semantic div
    return el
end