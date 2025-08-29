-- Smart Pins Vertical Spacing Adjustments
-- Fixes specific spacing patterns that look wrong in PDF output
-- 
-- Patterns handled:
-- 1. Paragraph ending with colon → List (reduce gap)
-- 2. Heading → Code block (pull together)
-- 
-- Tunable constants for easy adjustment:
local COLON_LIST_GAP = "-5pt"  -- Reduce space between colon and list
local HEADING_CODE_GAP = "-3pt" -- Pull heading and code together

function Blocks(blocks)
  local result = {}
  
  for i = 1, #blocks do
    local current = blocks[i]
    local next = blocks[i + 1]
    
    -- Always add the current block
    table.insert(result, current)
    
    -- Pattern 1: Paragraph ending with colon before list
    if current.t == "Para" then
      local text = pandoc.utils.stringify(current)
      if text:match(":$") and next and 
         (next.t == "BulletList" or next.t == "OrderedList") then
        -- Add spacing adjustment after the paragraph
        table.insert(result, pandoc.RawBlock('latex', 
          '\\vspace{' .. COLON_LIST_GAP .. '}% Pull list closer to colon'))
      end
      
    -- Pattern 2: Heading before code block
    elseif current.t == "Header" and next and next.t == "CodeBlock" then
      -- Add spacing adjustment after the heading
      table.insert(result, pandoc.RawBlock('latex', 
        '\\vspace{' .. HEADING_CODE_GAP .. '}% Pull code closer to heading'))
    end
    
    -- Future patterns can be added here:
    -- Pattern 3: [Description]
    -- elseif [condition] then
    --   table.insert(result, pandoc.RawBlock('latex', '\\vspace{...}'))
  end
  
  return result
end

return {
  {Blocks = Blocks}
}