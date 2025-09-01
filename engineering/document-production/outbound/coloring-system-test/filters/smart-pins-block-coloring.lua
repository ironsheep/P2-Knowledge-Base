-- Smart Pins 3-Block Coloring System
-- Maps markdown code block classes to colored tcolorbox environments
-- Configuration blocks (blue), Spin2 blocks (green), PASM2 blocks (yellow)

function CodeBlock(block)
  -- Check for class attributes
  local classes = block.classes
  local lang = block.attr and block.attr[1] or ""
  
  -- Configuration blocks: {.configuration} class -> ConfigBlock environment
  if classes and classes:includes("configuration") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{ConfigBlock}')
    local end_env = pandoc.RawBlock('latex', '\\end{ConfigBlock}')
    local content = pandoc.CodeBlock(block.text, block.attr)
    return {begin_env, content, end_env}
  
  -- Spin2 blocks: ```spin2 language tag -> Spin2Block environment  
  elseif block.attr and block.attr.classes and block.attr.classes:includes("spin2") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{Spin2Block}')
    local end_env = pandoc.RawBlock('latex', '\\end{Spin2Block}')
    local content = pandoc.CodeBlock(block.text, block.attr)
    return {begin_env, content, end_env}
    
  -- PASM2 blocks: ```pasm2 language tag -> PASM2Block environment
  elseif block.attr and block.attr.classes and block.attr.classes:includes("pasm2") then
    local begin_env = pandoc.RawBlock('latex', '\\begin{PASM2Block}')
    local end_env = pandoc.RawBlock('latex', '\\end{PASM2Block}')
    local content = pandoc.CodeBlock(block.text, block.attr)
    return {begin_env, content, end_env}
  
  -- Default: Let template handle (falls back to PASM2Block via Shaded environment)
  else
    return block
  end
end