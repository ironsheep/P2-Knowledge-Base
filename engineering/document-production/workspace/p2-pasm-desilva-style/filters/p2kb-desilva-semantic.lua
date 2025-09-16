--[[
DeSilva Semantic Blocks Lua Filter (ADAPTED FROM PROVEN SMART PINS)
Purpose: Convert markdown divs to LaTeX tcolorbox environments for DeSilva pedagogical elements
Created: 2025-09-16
Adapted from: Smart Pins p2kb-sp-semantic.lua (proven working)

Converts DeSilva pedagogical div types to corresponding LaTeX environments:
1. medicine-cabinet → dsmedicinecabinet (Solutions for common problems)
2. your-turn → dsyourturn (Hands-on exercises)
3. sidetrack → dssidetrack (Interesting but optional topics)
4. uff → dsuff (We just got through something complex)
5. well → dswell (Correcting common assumptions)
6. have-fun → dshavefun (Encouragement and celebration)

Also supports Smart Pins semantic elements for compatibility:
7. needs-diagram → gbdiagram
8. preliminary-content → gbpreliminary  
9. needs-verification → gbverify
10. needs-examples → gbexamples
11. needs-technical-review → gbtechreview
12. needs-code-review → gbcodereview
13. tip → gbtip
]]--

-- Mapping from div class names to LaTeX environment names
-- Using ds prefix for DeSilva elements, gb prefix for Smart Pins compatibility
local divMappings = {
    -- DeSilva pedagogical elements
    ["medicine-cabinet"] = "dsmedicinecabinet",
    ["your-turn"] = "dsyourturn", 
    ["sidetrack"] = "dssidetrack",
    ["uff"] = "dsuff",
    ["well"] = "dswell",
    ["have-fun"] = "dshavefun",
    
    -- Smart Pins compatibility (for shared content)
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