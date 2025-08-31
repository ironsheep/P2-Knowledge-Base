-- Pandoc Lua filter to convert div blocks to LaTeX environments
-- Version 2: Simpler, more direct approach

function Div(elem)
  -- Only process for LaTeX output
  if FORMAT ~= 'latex' then
    return elem
  end
  
  -- Get the first class if it exists
  local env = elem.classes[1]
  
  -- List of environments we want to convert
  local environments = {
    sidetrack = true,
    interlude = true,
    yourturn = true,
    missing = true,
    review = true,
    diagram = true,
    chapterend = true,
    notebox = true,
    tipbox = true,
    warningbox = true,
    cautionbox = true
  }
  
  -- If this div has a class we recognize, convert it
  if env and environments[env] then
    -- Create the LaTeX environment
    local latex_begin = pandoc.RawBlock('latex', '\\begin{' .. env .. '}')
    local latex_end = pandoc.RawBlock('latex', '\\end{' .. env .. '}')
    
    -- Return the environment with content
    local result = {latex_begin}
    for _, block in ipairs(elem.content) do
      table.insert(result, block)
    end
    table.insert(result, latex_end)
    
    return result
  end
  
  -- Return unchanged if not a recognized environment
  return elem
end