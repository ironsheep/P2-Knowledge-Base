-- P2KB Smart Pins - Fix Label Placement
-- Purpose: Ensure labels are inside the header commands, not outside
-- This fixes the malformed LaTeX that causes bracket issues
--
-- Version: 1.0
-- Date: 2025-09-04

function Header(header)
  -- For headers with identifiers (which become labels in LaTeX)
  if header.identifier and header.identifier ~= "" then
    -- Pandoc sometimes places labels outside the command
    -- We'll remove spaces/newlines from the content to prevent line breaks
    
    -- Get the text content
    local title = pandoc.utils.stringify(header.content)
    
    -- Remove any newlines that might have been introduced
    title = title:gsub("\n", " ")
    
    -- Create clean inline content
    header.content = {pandoc.Str(title)}
  end
  
  return header
end