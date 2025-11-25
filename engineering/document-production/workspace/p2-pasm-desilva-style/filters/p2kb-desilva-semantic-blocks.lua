-- P2KB DeSilva Semantic Blocks Lua Filter
-- Converts semantic div blocks to LaTeX environments for pedagogical elements
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - DeSilva Pedagogical Element Processing

-- Convert semantic div blocks to appropriate LaTeX environments
function Div(elem)
    local class = elem.classes[1]
    
    if class == "medicine" then
        -- Medicine Cabinet - Simpler alternatives when overwhelmed
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaMedicineCabinet}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaMedicineCabinet}")
        }
    elseif class == "yourturn" then
        -- Your Turn - Hands-on exercises
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaYourTurn}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaYourTurn}")
        }
    elseif class == "sidetrack" then
        -- Sidetrack - Interesting diversions and deeper explanations
        -- Extract the title from the first header inside the sidetrack
        local sidetrack_title = nil
        for _, block in ipairs(elem.content) do
            if block.t == "Header" then
                sidetrack_title = pandoc.utils.stringify(block.content)
                break
            end
        end

        -- Build result with TOC entry if we found a title
        local result = {}
        if sidetrack_title then
            -- Add TOC entry for sidetrack (indented, italic style)
            local toc_entry = string.format(
                "\\addcontentsline{toc}{section}{\\textit{Sidetrack: %s}}",
                sidetrack_title
            )
            table.insert(result, pandoc.RawBlock("latex", toc_entry))
        end
        table.insert(result, pandoc.RawBlock("latex", "\\begin{DeSilvaSidetrack}"))
        table.insert(result, elem)
        table.insert(result, pandoc.RawBlock("latex", "\\end{DeSilvaSidetrack}"))
        return result
    elseif class == "interlude" then
        -- Interlude - Stories and historical context
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaInterlude}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaInterlude}")
        }
    elseif class == "chapterend" then
        -- Chapter End - Summary and encouragement
        return {
            pandoc.RawBlock("latex", "\\begin{DeSilvaChapterEnd}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DeSilvaChapterEnd}")
        }
    elseif class == "commongotas" then
        -- Common Gotchas - Debugging help
        return {
            pandoc.RawBlock("latex", "\\begin{commongotas}"),
            elem,
            pandoc.RawBlock("latex", "\\end{commongotas}")
        }
    elseif class == "realworldexample" then
        -- Real-World Example - Practical applications
        return {
            pandoc.RawBlock("latex", "\\begin{realworldexample}"),
            elem,
            pandoc.RawBlock("latex", "\\end{realworldexample}")
        }
    elseif class == "performancenote" then
        -- Performance Notes - Optimization tips
        return {
            pandoc.RawBlock("latex", "\\begin{performancenote}"),
            elem,
            pandoc.RawBlock("latex", "\\end{performancenote}")
        }
    end
    
    -- Return unchanged if not a recognized semantic block type
    return elem
end