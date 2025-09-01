-- Smart Pins Colored Blocks System
-- Maps markdown code block classes to colored tcolorbox environments
-- 
-- Supported block types:
--   Configuration blocks (blue):   ```{.configuration} or auto-detect WRPIN:
--   Spin2 blocks (green):         ```spin2
--   PASM2 blocks (yellow):        ```pasm2  
--   Antipattern blocks (red):     ```{.antipattern}
--   Default blocks (gray):        ``` (no class)
--
-- Also handles:
--   - Decision tree flowchart boxes (start-box, decision-*, option groups)
--   - Smart page breaks between Parts and Chapters
--
-- Version: 1.0 - Renamed from smart-pins-block-coloring.lua
-- Date: 2025-08-29

-- Handle Div elements for flowchart boxes
function Div(div)
  local classes = div.classes
  
  -- Check for decision tree flowchart classes
  if classes:includes("start-box") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{startbox}')
    local end_env = pandoc.RawBlock('latex', '\\end{startbox}')
    return {begin_env, div, end_env}
  
  elseif classes:includes("decision-digital-out") or 
         classes:includes("decision-digital-in") or
         classes:includes("decision-analog-out") or
         classes:includes("decision-analog-in") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{decisioncategory}')
    local end_env = pandoc.RawBlock('latex', '\\end{decisioncategory}')
    return {begin_env, div, end_env}
  
  elseif classes:includes("pwm-subset") or
         classes:includes("serial-subset") or
         classes:includes("counting-subset") or
         classes:includes("timing-subset") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{optiongroup}')
    local end_env = pandoc.RawBlock('latex', '\\end{optiongroup}')
    return {begin_env, div, end_env}
  
  elseif classes:includes("columns") then
    -- Handle multi-column layout
    return div  -- Let LaTeX template handle columns
  end
  
  return div
end

-- Track if we just saw a Part header
local just_saw_part = false

-- Handle Header elements for page breaks
function Header(header)
  local title = pandoc.utils.stringify(header.content)
  
  -- Level 1 headers (Parts, Quick Reference, Index) always get page breaks
  if header.level == 1 then
    local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
    -- Mark that we just saw a Part
    if title:match("^Part") then
      just_saw_part = true
    else
      just_saw_part = false
    end
    return {pagebreak, header}
  
  -- Level 2 headers - check for specific patterns
  elseif header.level == 2 then
    -- Check if it's a chapter or appendix
    if title:match("^Chapter") or title:match("^Appendix") then
      -- Skip page break if this is the first chapter/appendix after a Part
      if just_saw_part then
        just_saw_part = false  -- Reset flag
        return header  -- No page break
      else
        -- Normal chapter/appendix - gets page break
        local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
        return {pagebreak, header}
      end
    -- Other level 2 headers that need page breaks
    elseif title:match("^Part") or
           title:match("Quick Reference") or
           title:match("^Index") then
      just_saw_part = false  -- Reset flag
      local pagebreak = pandoc.RawBlock('latex', '\\clearpage')
      return {pagebreak, header}
    end
  end
  
  -- Any other header type resets the flag
  just_saw_part = false
  return header
end

function CodeBlock(block)
  -- Check for class attributes
  local classes = block.classes
  local lang = block.attr and block.attr[1] or ""
  
  -- Antipattern blocks: ```{.antipattern} -> AntipatternBlock environment (RED)
  if classes and classes:includes("antipattern") then
    -- Return complete LaTeX block for antipattern styling
    local latex_block = '\\begin{AntipatternBlock}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                       block.text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{AntipatternBlock}'
    return pandoc.RawBlock('latex', latex_block)
  
  -- Configuration blocks: detect by WRPIN: pattern OR {.configuration} class
  -- These are the mode configuration blocks showing WRPIN/WXPIN/WYPIN settings
  elseif (classes and classes:includes("configuration")) or 
         block.text:match("^WRPIN:") or 
         block.text:match("\nWRPIN:") then
    -- Return complete LaTeX block to bypass Shaded environment
    local latex_block = '\\begin{ConfigBlock}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                       block.text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{ConfigBlock}'
    return pandoc.RawBlock('latex', latex_block)
  
  -- Spin2 blocks: ```spin2 language tag -> Spin2Block environment  
  elseif block.attr and block.attr.classes and block.attr.classes:includes("spin2") then
    -- Return complete LaTeX block to bypass Shaded environment
    local latex_block = '\\begin{Spin2Block}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                       block.text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{Spin2Block}'
    return pandoc.RawBlock('latex', latex_block)
    
  -- PASM2 blocks: ```pasm2 language tag -> PASM2Block environment
  elseif block.attr and block.attr.classes and block.attr.classes:includes("pasm2") then
    -- Return complete LaTeX block with proper lstlisting settings
    local latex_block = '\\begin{PASM2Block}\n' ..
                       '\\lstset{language=pasm2,basicstyle=\\ttfamily,keywordstyle=\\bfseries\\uppercase,' ..
                       'numbers=left,numberstyle=\\tiny,xleftmargin=15pt,frame=none,backgroundcolor=\\color{white}}\n' ..
                       '\\begin{lstlisting}\n' ..
                       block.text .. '\n' ..
                       '\\end{lstlisting}\n' ..
                       '\\end{PASM2Block}'
    return pandoc.RawBlock('latex', latex_block)
  
  -- Default: Untagged blocks get gray treatment
  else
    -- Return complete LaTeX block for default gray styling
    return block  -- Let Pandoc handle default formatting
  end
end