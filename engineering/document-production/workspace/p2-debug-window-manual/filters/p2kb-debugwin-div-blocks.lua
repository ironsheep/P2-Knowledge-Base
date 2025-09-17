-- P2KB Debug Window Div Blocks Lua Filter
-- Converts div-syntax code blocks to LaTeX environments for 5-color system
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - Debug Window 5-Color Code Block Processing
-- Based on: p2kb-desilva-div-blocks.lua (proven working)

-- Convert div blocks to appropriate LaTeX environments
function Div(elem)
    local class = elem.classes[1]
    
    -- Standard code blocks
    if class == "spin2" then
        -- Spin2 high-level language (green)
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinSpin2Block}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinSpin2Block}")
        }
    elseif class == "pasm2" then
        -- PASM2 assembly language (yellow/cream)
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinPASM2Block}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinPASM2Block}")
        }
    elseif class == "debug" then
        -- DEBUG() statements (blue) - Most common in debug manual
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinDebugBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinDebugBlock}")
        }
    elseif class == "terminal" then
        -- Terminal window output (gray)
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinTerminalBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinTerminalBlock}")
        }
    
    -- Window-specific command blocks (all use purple theme)
    elseif class == "bitmap" then
        -- Bitmap window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinBitmapBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinBitmapBlock}")
        }
    elseif class == "scope" then
        -- Scope window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinScopeBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinScopeBlock}")
        }
    elseif class == "logic" then
        -- Logic analyzer window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinLogicBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinLogicBlock}")
        }
    elseif class == "plot" then
        -- Plot window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinPlotBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinPlotBlock}")
        }
    elseif class == "fft" then
        -- FFT window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinFFTBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinFFTBlock}")
        }
    elseif class == "spectro" then
        -- Spectro window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinSpectroBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinSpectroBlock}")
        }
    elseif class == "scope_xy" or class == "scopexy" then
        -- Scope XY window commands
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinScopeXYBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinScopeXYBlock}")
        }
    
    -- Generic window commands (catch-all)
    elseif class == "window" then
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinWindowBlock}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinWindowBlock}")
        }
    end
    
    -- Return unchanged if not a recognized code block type
    return elem
end

-- Process CodeBlock elements for any that might not be in divs
-- This handles legacy language-tagged blocks if any remain
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
    elseif lang == "debug" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "debug"}
        )
    elseif lang == "terminal" then
        return pandoc.Div(
            {pandoc.CodeBlock(elem.text, elem.attr)},
            {class = "terminal"}
        )
    end
    
    -- Return unchanged if not a recognized type
    return elem
end