-- Smart Pins Div-Based Colored Blocks System
-- Maps markdown div-wrapped code blocks to colored tcolorbox environments
-- 
-- Supported div block types (3-color pedagogical system):
--   Spin2 blocks (green):         :::: spin2 (includes configuration)
--   PASM2 blocks (yellow):        :::: pasm2  
--   Antipattern blocks (red):     :::: antipattern
--
-- Also handles:
--   - Decision tree flowchart boxes (start-box, decision-*, option groups)
--   - Smart page breaks between Parts and Chapters
--
-- Version: 2.0 - Converted from CodeBlock to Div processing
-- Date: 2025-08-31

-- Handle Div elements for both code blocks and flowchart boxes
function Div(div)
  local classes = div.classes
  
  -- ===== CODE BLOCK DIVS (3-color system) =====
  
  -- Antipattern blocks: :::: antipattern -> AntipatternBlock environment (RED)
  if classes:includes("antipattern") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block for antipattern styling
      local latex_block = '\\begin{AntipatternBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{AntipatternBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- Spin2 blocks: :::: spin2 -> Spin2Block environment (GREEN)
  -- Note: This includes configuration blocks (WRPIN:/WXPIN:/WYPIN:) per pedagogical decision
  elseif classes:includes("spin2") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block for Spin2 styling
      local latex_block = '\\begin{Spin2Block}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{Spin2Block}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- PASM2 blocks: :::: pasm2 -> PASM2Block environment (YELLOW)
  elseif classes:includes("pasm2") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block with proper lstlisting settings
      local latex_block = '\\begin{PASM2Block}\n' ..
                         '\\lstset{language=pasm2,basicstyle=\\ttfamily,keywordstyle=\\bfseries\\uppercase,' ..
                         'numbers=left,numberstyle=\\tiny,xleftmargin=15pt,frame=none,backgroundcolor=\\color{white}}\n' ..
                         '\\begin{lstlisting}\n' ..
                         code_block.text .. '\n' ..
                         '\\end{lstlisting}\n' ..
                         '\\end{PASM2Block}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- ===== FLOWCHART/DECISION TREE DIVS =====
  
  elseif classes:includes("start-box") then
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

-- No longer processing CodeBlock elements directly
-- All code blocks must be wrapped in divs for processing