-- P2KB DeSilva Div Blocks Lua Filter
-- Converts div-syntax code blocks to LaTeX environments for 5-color system
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - DeSilva 5-Color Code Block Processing

-- Convert div blocks to appropriate LaTeX environments
function Div(elem)
    local class = elem.classes[1]
    
    if class == "spin2" then
        -- Spin2 high-level language (green)
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaSpin2Block}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaSpin2Block}")
        }
    elseif class == "pasm2" then
        -- PASM2 assembly language (yellow/cream) - Most common
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaPASM2Block}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaPASM2Block}")
        }
    elseif class == "cordic" then
        -- CORDIC mathematical operations (purple)
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaCORDICBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaCORDICBlock}")
        }
    elseif class == "multicog" then
        -- Multi-COG parallel processing (blue)
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaMultiCOGBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaMultiCOGBlock}")
        }
    elseif class == "antipattern" then
        -- What NOT to do (red)
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaAntipatternBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaAntipatternBlock}")
        }
    end
    
    -- Return unchanged if not a recognized code block type
    return elem
end

-- Process CodeBlock elements for any that might not be in divs
function CodeBlock(elem)
    local lang = elem.classes[1]
    
    if lang == "spin2" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "spin2"}
        )
    elseif lang == "pasm2" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "pasm2"}
        )
    elseif lang == "cordic" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "cordic"}
        )
    elseif lang == "multicog" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "multicog"}
        )
    elseif lang == "antipattern" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "antipattern"}
        )
    end
    
    -- Return unchanged for other languages
    return elem
end