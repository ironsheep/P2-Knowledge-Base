-- Lua filter to convert Pandoc div syntax to LaTeX environments
-- Usage: pandoc ... --lua-filter=div-to-environment.lua

function Div(elem)
  -- Only process for LaTeX output
  if FORMAT ~= 'latex' then
    return elem
  end
  
  -- Get the first class if it exists
  local env = elem.classes[1]
  
  -- Define which divs should become environments
  local environments = {
    sidetrack = true,
    interlude = true,
    yourturn = true,
    missing = true,
    review = true,
    diagram = true,
    chapterend = true
  }
  
  -- If this div class should be an environment
  if env and environments[env] then
    -- Create LaTeX environment
    local latex_begin = pandoc.RawBlock('latex', '\\begin{' .. env .. '}')
    local latex_end = pandoc.RawBlock('latex', '\\end{' .. env .. '}')
    
    -- Get the content blocks
    local content = elem.content
    
    -- Return the environment with content
    local result = {latex_begin}
    for _, block in ipairs(content) do
      table.insert(result, block)
    end
    table.insert(result, latex_end)
    
    return result
  end
  
  -- Return unchanged if not a special environment
  return elem
end