-- Smart Pins Unified Styling Filter
-- Combines three-color system with heading-aware indentation
-- Configuration (blue), Spin2 (green), PASM2 (yellow) + proper alignment

local current_level = 1  -- Track current heading level

function Header(elem)
  -- Update current level when we encounter headers
  current_level = elem.level
  return elem
end

function CodeBlock(block)
  -- Determine the color environment based on language
  local color_env = ""
  local indent_level = ""
  
  -- Color selection based on language markers
  if block.attr and block.attr.classes then
    if block.attr.classes:includes("spin2") then
      color_env = "Spin2Block"  -- Green
    elseif block.attr.classes:includes("pasm2") then
      color_env = "PASM2Block"  -- Yellow
    elseif block.attr.classes:includes("configuration") then
      color_env = "ConfigBlock"  -- Blue
    else
      -- Unmarked blocks default to ConfigBlock (blue)
      color_env = "ConfigBlock"
    end
  else
    -- No language marker = Configuration block
    color_env = "ConfigBlock"
  end
  
  -- Indentation based on heading level
  -- Level 1 (Part/Chapter) = no extra indent
  -- Level 2 (Section) = indent level 2
  -- Level 3+ (Subsection) = indent level 3
  if current_level == 2 then
    indent_level = "Level2"
  elseif current_level >= 3 then
    indent_level = "Level3"
  else
    indent_level = ""  -- No suffix for level 1
  end
  
  -- Combine color and indent into environment name
  -- E.g., "Spin2Block", "Spin2BlockLevel2", "ConfigBlockLevel3"
  local env_name = color_env .. indent_level
  
  -- Check if this combined environment exists in the template
  -- For now, we'll just use the color environment and add spacing
  -- This can be enhanced later with proper combined environments
  
  local begin_env = pandoc.RawBlock('latex', '\\begin{' .. color_env .. '}')
  local end_env = pandoc.RawBlock('latex', '\\end{' .. color_env .. '}')
  
  -- If we need indentation, add it as spacing before the environment
  local indent_space = ""
  if indent_level == "Level2" then
    indent_space = pandoc.RawBlock('latex', '\\hspace*{15pt}')  -- Indent for section level
  elseif indent_level == "Level3" then
    indent_space = pandoc.RawBlock('latex', '\\hspace*{30pt}')  -- More indent for subsection
  end
  
  local content = pandoc.CodeBlock(block.text, block.attr)
  
  if indent_space ~= "" then
    return {indent_space, begin_env, content, end_env}
  else
    return {begin_env, content, end_env}
  end
end