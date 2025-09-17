-- P2KB Debug Window Semantic Blocks Lua Filter
-- Converts semantic div blocks to LaTeX environments for debug window elements
-- Author: Iron Sheep Productions, LLC
-- Version: 1.0 - Debug Window Semantic Element Processing
-- Based on: p2kb-desilva-semantic.lua (proven working)

-- Convert semantic div blocks to LaTeX environments
function Div(elem)
    local class = elem.classes[1]
    
    -- Discovery boxes (major findings)
    if class == "discovery" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwdiscovery}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwdiscovery}")
        }
    
    -- Experiment boxes (hands-on learning)
    elseif class == "experiment" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwexperiment}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwexperiment}")
        }
    
    -- Performance notes (optimization tips)
    elseif class == "performance" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwperformance}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwperformance}")
        }
    
    -- Pro tips (advanced techniques)
    elseif class == "tip" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwtip}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwtip}")
        }
    
    -- Screenshot boxes (annotated images)
    elseif class == "screenshot" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwscreenshot}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwscreenshot}")
        }
    
    -- Needs screenshot placeholder
    elseif class == "needs-screenshot" then
        return {
            pandoc.RawBlock("latex", "\\begin{dwneedsscreenshot}"),
            elem,
            pandoc.RawBlock("latex", "\\end{dwneedsscreenshot}")
        }
    
    -- Performance comparison boxes
    elseif class == "performance-comparison" or class == "comparison" then
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinComparison}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinComparison}")
        }
    
    -- Multi-channel/multi-window coordination
    elseif class == "multichannel" or class == "multiwindow" then
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinMultiChannel}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinMultiChannel}")
        }
    
    -- Window gallery (showing multiple window types)
    elseif class == "gallery" then
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinGallery}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinGallery}")
        }
    
    -- Command reference boxes
    elseif class == "commandref" or class == "reference" then
        return {
            pandoc.RawBlock("latex", "\\begin{DebugWinCommandRef}"),
            elem,
            pandoc.RawBlock("latex", "\\end{DebugWinCommandRef}")
        }
    end
    
    -- Return unchanged if not a recognized semantic type
    return elem
end