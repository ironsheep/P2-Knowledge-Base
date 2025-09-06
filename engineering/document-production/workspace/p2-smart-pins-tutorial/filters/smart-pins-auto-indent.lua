-- Smart Pins Auto-Indent Lua Filter (Minimal)
-- Convert code blocks to RawBlock with LaTeX environments directly

local current_level = 1

function Header(elem)
  current_level = elem.level
  return elem
end

function CodeBlock(elem)
  local env_name
  
  if current_level <= 1 then
    env_name = "Shaded"
  elseif current_level == 2 then
    env_name = "CodeLevel2"
  else
    env_name = "CodeLevel3"
  end
  
  -- Convert directly to LaTeX RawBlock to avoid Div issues
  local latex_begin = "\\begin{" .. env_name .. "}\n\\begin{verbatim}\n"
  local latex_end = "\n\\end{verbatim}\n\\end{" .. env_name .. "}"
  local latex_content = latex_begin .. elem.text .. latex_end
  
  return pandoc.RawBlock("latex", latex_content)
end