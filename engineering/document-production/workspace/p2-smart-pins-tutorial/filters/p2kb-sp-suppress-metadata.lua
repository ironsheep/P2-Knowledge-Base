-- P2KB Smart Pins - Suppress Metadata Headers
-- Purpose: Remove version and creation date headers that appear after title
-- These should not become sections in the PDF
--
-- Version: 1.0
-- Date: 2025-09-04

function Header(header)
  local title = pandoc.utils.stringify(header)
  
  -- Suppress specific metadata headers that shouldn't be sections
  if header.level == 3 then
    -- Check for version metadata
    if title:match("^Version %d+%.%d+") or 
       title:match("^Created:") or
       title:match("Green Book Edition") then
      -- Return empty block to suppress these headers
      return {}
    end
  end
  
  return header
end