-- Smart Pins 4-Block Coloring System
-- Maps markdown code block classes to colored tcolorbox environments
-- Configuration blocks (blue), Spin2 blocks (green), PASM2 blocks (yellow), Antipattern blocks (red)

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

-- This filter handles ONLY code block coloring
-- Page breaks are handled by part-chapter-pagebreaks.lua

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
    -- Return complete LaTeX block to bypass Shaded environment
    -- Use Verbatim like the other blocks to avoid white background
    local latex_block = '\\begin{PASM2Block}\n' ..
                       '\\begin{Verbatim}[numbers=left,numbersep=5pt,xleftmargin=15pt]\n' ..
                       block.text .. '\n' ..
                       '\\end{Verbatim}\n' ..
                       '\\end{PASM2Block}'
    return pandoc.RawBlock('latex', latex_block)
  
  -- Default: Untagged blocks get gray treatment
  else
    -- Return complete LaTeX block for default gray styling
    return block  -- Let Pandoc handle default formatting
  end
end