-- P2KB DeSilva - Code Coloring Filter (ADAPTED FROM PROVEN SMART PINS)
-- Purpose: ONLY handles code block coloring for div-wrapped blocks
-- No pagination - single responsibility
--
-- Supported div block types (5-color DeSilva pedagogical system):
--   Spin2 blocks (green):         ::: spin2 (includes configuration)
--   PASM2 blocks (yellow):        ::: pasm2  
--   CORDIC blocks (purple):       ::: cordic (hardware math operations)
--   Multi-COG blocks (blue):      ::: multicog (parallel processing)
--   Antipattern blocks (red):     ::: antipattern
--
-- Also handles DeSilva pedagogical elements:
--   Medicine Cabinet, Your Turn, Sidetrack, etc.
--
-- Version: 1.0 - Adapted from Smart Pins p2kb-sp-code-coloring.lua
-- Date: 2025-09-16
-- Source: Proven Smart Pins workspace filter (3-color -> 5-color expansion)

-- Handle Div elements for code blocks and pedagogical elements
function Div(div)
  local classes = div.classes
  
  -- ===== CODE BLOCK DIVS (5-color DeSilva system) =====
  
  -- Antipattern blocks: ::: antipattern -> DeSilvaAntipatternBlock environment (RED)
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
      local latex_block = '\\begin{DeSilvaAntipatternBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{DeSilvaAntipatternBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- Spin2 blocks: ::: spin2 -> DeSilvaSpin2Block environment (GREEN)
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
      local latex_block = '\\begin{DeSilvaSpin2Block}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{DeSilvaSpin2Block}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- PASM2 blocks: ::: pasm2 -> DeSilvaPASM2Block environment (YELLOW)
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
      -- Return complete LaTeX block using Verbatim (mnemonics already uppercased by mnemonic filter)
      local latex_block = '\\begin{DeSilvaPASM2Block}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{DeSilvaPASM2Block}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- CORDIC blocks: ::: cordic -> DeSilvaCORDICBlock environment (PURPLE)
  elseif classes:includes("cordic") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block for CORDIC styling
      local latex_block = '\\begin{DeSilvaCORDICBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{DeSilvaCORDICBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
    
  -- Multi-COG blocks: ::: multicog -> DeSilvaMultiCOGBlock environment (BLUE)
  elseif classes:includes("multicog") then
    -- Find the CodeBlock inside this div
    local code_block = nil
    pandoc.walk_block(div, {
      CodeBlock = function(cb)
        code_block = cb
        return cb
      end
    })
    
    if code_block then
      -- Return complete LaTeX block for Multi-COG styling
      local latex_block = '\\begin{DeSilvaMultiCOGBlock}\n' ..
                         '\\begin{Verbatim}[numbers=left,numbersep=8pt,xleftmargin=-10pt]\n' ..
                         code_block.text .. '\n' ..
                         '\\end{Verbatim}\n' ..
                         '\\end{DeSilvaMultiCOGBlock}'
      return pandoc.RawBlock('latex', latex_block)
    end
  
  -- ===== DESILVA PEDAGOGICAL ELEMENTS =====
  
  elseif classes:includes("medicine-cabinet") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsmedicinecabinet}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsmedicinecabinet}'))
    return result

  elseif classes:includes("your-turn") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsyourturn}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsyourturn}'))
    return result

  elseif classes:includes("sidetrack") then
    -- Extract title from first heading in sidetrack for TOC entry
    local sidetrack_title = nil
    for _, block in ipairs(div.content) do
      if block.t == "Header" then
        sidetrack_title = pandoc.utils.stringify(block.content)
        break
      end
    end

    local result = {pandoc.RawBlock('latex', '\\begin{dssidetrack}')}
    -- Add TOC entry if we found a title
    if sidetrack_title then
      table.insert(result, pandoc.RawBlock('latex',
        '\\addcontentsline{toc}{section}{Sidetrack: ' .. sidetrack_title .. '}'))
    end
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dssidetrack}'))
    return result

  elseif classes:includes("uff") then
    local result = {pandoc.RawBlock('latex', '\\begin{dsuff}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dsuff}'))
    return result

  elseif classes:includes("well") then
    local result = {pandoc.RawBlock('latex', '\\begin{dswell}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dswell}'))
    return result

  elseif classes:includes("have-fun") then
    local result = {pandoc.RawBlock('latex', '\\begin{dshavefun}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{dshavefun}'))
    return result

  elseif classes:includes("interlude") then
    local result = {pandoc.RawBlock('latex', '\\begin{DeSilvaInterlude}')}
    for _, block in ipairs(div.content) do
      table.insert(result, block)
    end
    table.insert(result, pandoc.RawBlock('latex', '\\end{DeSilvaInterlude}'))
    return result
  end

  -- Return div unchanged if not a recognized type
  return div
end

-- NO Header function - pagination is handled by separate filter
-- NO CodeBlock function - all code blocks must be wrapped in divs