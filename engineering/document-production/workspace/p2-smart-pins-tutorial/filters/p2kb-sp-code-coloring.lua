-- P2KB Smart Pins - Code Coloring Filter
-- Purpose: ONLY handles code block coloring for div-wrapped blocks
-- No pagination - single responsibility
--
-- Supported div block types (3-color pedagogical system):
--   Spin2 blocks (green):         ::: spin2 (includes configuration)
--   PASM2 blocks (yellow):        ::: pasm2  
--   Antipattern blocks (red):     ::: antipattern
--
-- Also handles decision tree flowchart boxes
--
-- Version: 1.0 - Extracted from smart-pins-div-blocks.lua
-- Date: 2025-09-04

-- Handle Div elements for code blocks and flowchart boxes
function Div(div)
  local classes = div.classes
  
  -- ===== CODE BLOCK DIVS (3-color system) =====
  
  -- Antipattern blocks: ::: antipattern -> AntipatternBlock environment (RED)
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
  
  -- Spin2 blocks: ::: spin2 -> Spin2Block environment (GREEN)
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
    
  -- PASM2 blocks: ::: pasm2 -> PASM2Block environment (YELLOW)
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
  
  elseif classes:includes("option-box-yes") or
         classes:includes("option-box-no") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{optionbox}')
    local end_env = pandoc.RawBlock('latex', '\\end{optionbox}')
    return {begin_env, div, end_env}
  
  elseif classes:includes("option-group") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{optiongroup}')
    local end_env = pandoc.RawBlock('latex', '\\end{optiongroup}')
    return {begin_env, div, end_env}
  
  elseif classes:includes("decision-box-input") or
         classes:includes("decision-box-output") or
         classes:includes("decision-box-special") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{decisionbox}')
    local end_env = pandoc.RawBlock('latex', '\\end{decisionbox}')
    return {begin_env, div, end_env}
  end
  
  -- Return div unchanged if not a recognized type
  return div
end

-- NO Header function - pagination is handled by p2kb-sp-pagination.lua
-- NO CodeBlock function - all code blocks must be wrapped in divs