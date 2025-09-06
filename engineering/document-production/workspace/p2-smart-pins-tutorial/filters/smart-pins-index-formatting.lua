-- Smart Pins Index Formatting
-- Converts bulleted index entries to proper index format
-- 
-- Index entries should appear as:
-- - No bullets
-- - Hanging indent
-- - Each entry on its own line

local in_index = false

function Header(elem)
  local title = pandoc.utils.stringify(elem)
  
  -- Check if we're entering or leaving the Index
  if elem.level == 2 and title:match("^Index") then
    in_index = true
  elseif elem.level == 2 and in_index then
    -- We've left the index section
    in_index = false
  end
  
  return elem
end

function BulletList(elem)
  -- Only process bullet lists in the index section
  if not in_index then
    return elem
  end
  
  -- Convert bullet list to formatted index entries
  local blocks = {}
  
  for _, item in ipairs(elem.content) do
    -- Get the content of the list item
    local item_text = pandoc.utils.stringify(item)
    
    -- Create a hanging indent paragraph for each index entry
    -- Using LaTeX commands for proper index formatting
    local latex_entry = string.format('\\noindent\\hangindent=2em %s\\par', item_text)
    table.insert(blocks, pandoc.RawBlock('latex', latex_entry))
  end
  
  return blocks
end

function Para(elem)
  -- In the index, handle the letter group headers specially
  if in_index then
    local text = pandoc.utils.stringify(elem)
    -- Check if this is a single bold letter (like **A**)
    if text:match("^[A-Z]$") and elem.content[1] and elem.content[1].t == "Strong" then
      -- Add some space before letter groups (except the first)
      return {
        pandoc.RawBlock('latex', '\\vspace{0.5em}'),
        elem
      }
    end
  end
  return elem
end

return {
  {Header = Header},
  {Para = Para},
  {BulletList = BulletList}
}