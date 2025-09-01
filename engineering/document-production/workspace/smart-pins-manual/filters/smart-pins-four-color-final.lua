-- Smart Pins 4-Color System FINAL
-- Configuration blocks: ```configuration -> Blue ConfigBlock
-- Spin2 blocks: ```spin2 -> Green Spin2Block  
-- PASM2 blocks: ```pasm2 -> Yellow PASM2Block
-- All other code blocks -> Gray (default lstlisting)

function CodeBlock(block)
  -- Check for language class in code block
  if block.attr and block.attr.classes then
    
    -- Configuration blocks: ```configuration -> ConfigBlock (BLUE)
    if block.attr.classes:includes("configuration") then
      local begin_env = pandoc.RawBlock('latex', '\\begin{ConfigBlock}')
      local end_env = pandoc.RawBlock('latex', '\\end{ConfigBlock}')
      local content = pandoc.CodeBlock(block.text, block.attr)
      return {begin_env, content, end_env}
    
    -- Spin2 blocks: ```spin2 -> Spin2Block (GREEN)  
    elseif block.attr.classes:includes("spin2") then
      local begin_env = pandoc.RawBlock('latex', '\\begin{Spin2Block}')
      local end_env = pandoc.RawBlock('latex', '\\end{Spin2Block}')
      local content = pandoc.CodeBlock(block.text, block.attr)
      return {begin_env, content, end_env}
      
    -- PASM2 blocks: ```pasm2 -> PASM2Block (YELLOW)
    elseif block.attr.classes:includes("pasm2") then
      local begin_env = pandoc.RawBlock('latex', '\\begin{PASM2Block}')
      local end_env = pandoc.RawBlock('latex', '\\end{PASM2Block}')
      local content = pandoc.CodeBlock(block.text, block.attr)
      return {begin_env, content, end_env}
    end
  end
  
  -- Default: All other code blocks stay as regular lstlisting (GRAY)
  return block
end