-- Smart Pins Auto-Indent Lua Filter
-- Automatically converts code blocks to level-appropriate environments
-- Based on heading level and list context

local current_level = 1  -- Track current heading level
local in_list = false    -- Track if we're inside a list
local list_depth = 0     -- Track nested list depth

function Header(elem)
  -- Update current level when we encounter headers
  current_level = elem.level
  return elem
end

function OrderedList(elem)
  -- Track entering ordered lists
  in_list = true
  list_depth = list_depth + 1
  
  -- Process the list content with list context
  local processed = pandoc.walk_block(elem, {
    CodeBlock = function(code)
      return CodeBlockInList(code)
    end,
    OrderedList = function(nested_list)
      list_depth = list_depth + 1
      local result = pandoc.walk_block(nested_list, {CodeBlock = CodeBlockInList})
      list_depth = list_depth - 1
      return result
    end,
    BulletList = function(nested_list)
      list_depth = list_depth + 1
      local result = pandoc.walk_block(nested_list, {CodeBlock = CodeBlockInList})
      list_depth = list_depth - 1
      return result
    end
  })
  
  list_depth = list_depth - 1
  if list_depth == 0 then
    in_list = false
  end
  
  return processed
end

function BulletList(elem)
  -- Track entering bullet lists (same logic as ordered lists)
  in_list = true
  list_depth = list_depth + 1
  
  local processed = pandoc.walk_block(elem, {
    CodeBlock = function(code)
      return CodeBlockInList(code)
    end,
    OrderedList = function(nested_list)
      list_depth = list_depth + 1
      local result = pandoc.walk_block(nested_list, {CodeBlock = CodeBlockInList})
      list_depth = list_depth - 1
      return result
    end,
    BulletList = function(nested_list)
      list_depth = list_depth + 1
      local result = pandoc.walk_block(nested_list, {CodeBlock = CodeBlockInList})
      list_depth = list_depth - 1
      return result
    end
  })
  
  list_depth = list_depth - 1
  if list_depth == 0 then
    in_list = false
  end
  
  return processed
end

function CodeBlockInList(elem)
  -- Handle code blocks inside lists with proper indentation
  local env_name
  local indent_class = ""
  
  -- Base environment selection by heading level
  if current_level <= 1 then
    env_name = "Shaded"
  elseif current_level == 2 then
    env_name = "CodeLevel2"
  elseif current_level >= 3 then
    env_name = "CodeLevel3"
  end
  
  -- Add list indentation modifier
  if list_depth > 0 then
    indent_class = "list-indent-" .. list_depth
  end
  
  -- Return with both environment and list context
  local classes = {env_name}
  if indent_class ~= "" then
    table.insert(classes, indent_class)
  end
  
  return pandoc.Div({elem}, {class = classes})
end

function CodeBlock(elem)
  -- Handle code blocks outside lists
  if in_list then
    -- This shouldn't happen due to list processing, but safety check
    return CodeBlockInList(elem)
  end
  
  local env_name
  
  if current_level <= 1 then
    env_name = "Shaded"        -- Chapter level - use enhanced default
  elseif current_level == 2 then
    env_name = "CodeLevel2"    -- Section level - indent
  elseif current_level >= 3 then
    env_name = "CodeLevel3"    -- Subsection+ level - double indent
  end
  
  -- Return as custom div with the appropriate environment
  return pandoc.Div({elem}, {class = env_name})
end

function Div(elem)
  -- Handle existing divs - don't double-process
  if elem.classes and #elem.classes > 0 then
    local class = elem.classes[1]
    if class == "CodeLevel2" or class == "CodeLevel3" or class == "tryityourself" then
      -- Already has custom class, leave alone
      return elem
    end
  end
  
  -- Process any code blocks inside regular divs
  return pandoc.walk_block(elem, {CodeBlock = CodeBlock})
end