-- De Silva Div to Environment Lua Filter
-- Converts Pandoc div blocks to LaTeX environments for pedagogical elements
-- Usage: --lua-filter=desilva-div-to-environment

function Div(elem)
  -- Get the first class from the div
  local class = elem.classes[1]
  
  if not class then
    return elem
  end
  
  -- Map div classes to De Silva environments
  local environment_map = {
    sidetrack = "sidetrack",
    interlude = "interlude", 
    yourturn = "yourturn",
    chapterend = "chapterend",
    missing = "missing",
    review = "review",
    diagram = "diagram"
  }
  
  local env_name = environment_map[class]
  
  if env_name then
    -- Convert div to LaTeX environment
    local begin_env = pandoc.RawBlock('latex', '\\begin{' .. env_name .. '}')
    local end_env = pandoc.RawBlock('latex', '\\end{' .. env_name .. '}')
    
    -- Return the environment with content inside
    local content = {begin_env}
    for i, block in ipairs(elem.content) do
      table.insert(content, block)
    end
    table.insert(content, end_env)
    
    return content
  end
  
  -- Return unchanged if not a recognized class
  return elem
end